/* Independent, bounded downloads. A failed manual never discards drawing results. */
((root)=>{
  'use strict';
  function create({fetch:request=root.fetch.bind(root),timeout=30000,setTimer=root.setTimeout.bind(root),clearTimer=root.clearTimeout.bind(root)}={}){
    const states={core:{status:'idle',value:null},manual:{status:'idle',value:null}},listeners=new Set();
    let lastCore,lastManual,combined=[];
    const emit=()=>{for(const listener of listeners)listener();};
    function load(key,version){
      const state=states[key];if(state.status==='ready')return Promise.resolve(state.value);if(state.pending)return state.pending;
      const core=states.core.value;
      if(key==='manual'&&!core)return load('core',version).then(()=>load('manual',version));
      const path=key==='core'?'registers/io-search-index.json':core.manual_path;
      state.status='loading';state.error=null;
      state.pending=(async()=>{
        const controller=new AbortController();let timer;
        try{
          const work=(async()=>{
            const response=await request(path+'?v='+encodeURIComponent(version),{signal:controller.signal});
            if(!response.ok)throw new Error('HTTP '+response.status);
            const value=await response.json();
            if(value.version!==version||!Array.isArray(value.records))throw new Error('자료 버전이 다릅니다. 새로고침해 주세요.');
            if(key==='core'){
              if(value.schema_version!==2||!value.build_id||value.manual_path!=='registers/io-search-manual.json'||!value.counts||value.records.some(r=>r.kind==='manual'))throw new Error('검색 자료 형식 오류');
            }else if(value.schema_version!==1||value.build_id!==core.build_id||value.records.length!==core.counts.manual||value.records.some(r=>r.kind!=='manual'))throw new Error('추가 자료가 현재 검색 색인과 다릅니다. 새로고침해 주세요.');
            return value;
          })();
          const value=await Promise.race([work,new Promise((_,reject)=>{timer=setTimer(()=>{controller.abort();reject(new Error('자료 응답 시간이 초과되었습니다.'));},timeout);})]);
          state.value=value;state.status='ready';return value;
        }catch(error){state.status='error';state.error=error;throw error;}
        finally{clearTimer(timer);state.pending=null;emit();}
      })();
      emit();return state.pending;
    }
    return {states,load,subscribe(listener){listeners.add(listener);return ()=>listeners.delete(listener);},records(kind=''){
      const core=states.core.value?.records||[],manual=states.manual.value?.records||[];
      if(kind==='manual')return manual;if(kind||!manual.length)return core;
      if(core!==lastCore||manual!==lastManual){combined=core.concat(manual);lastCore=core;lastManual=manual;}
      return combined;
    }};
  }
  root.GMEIOSearchLoader={create};
})(globalThis);

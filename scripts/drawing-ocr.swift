import Foundation
import Vision
import AppKit
let argv = CommandLine.arguments
let imagePath = argv[1]
let image = NSImage(contentsOfFile: imagePath)!
var rect = CGRect(origin: .zero, size: image.size)
let cg = image.cgImage(forProposedRect: &rect, context: nil, hints: nil)!
let req = VNRecognizeTextRequest()
req.recognitionLevel = .accurate
req.recognitionLanguages = ["en-US"]
req.usesLanguageCorrection = false
req.minimumTextHeight = 0.001
let handler = VNImageRequestHandler(cgImage: cg, options: [:])
try handler.perform([req])
let tokenRegex = try NSRegularExpression(pattern: #"(?<![A-Za-z0-9.])(?:[0-9]+[A-Z]{1,4}[0-9]+|[0-9]+\.[0-9]+)(?![A-Za-z0-9.])"#)
func boxArray(_ box: CGRect) -> [Double] { return [box.minX,1-box.maxY,box.maxX,1-box.minY] }
let result = (req.results ?? []).map { observation -> [String:Any] in
 let box = observation.boundingBox
 let top = observation.topCandidates(1).first!
 let tokens: [[String:Any]] = tokenRegex.matches(in:top.string,range:NSRange(top.string.startIndex...,in:top.string)).compactMap { match in
  guard let range = Range(match.range,in:top.string),let tokenBox = try? top.boundingBox(for:range) else { return nil }
  return ["text":String(top.string[range]),"confidence":top.confidence,"bbox":boxArray(tokenBox.boundingBox)]
 }
 return ["tokens":tokens,"candidates": observation.topCandidates(3).map { ["text":$0.string,"confidence":$0.confidence] }, "bbox":[box.minX,1-box.maxY,box.maxX,1-box.minY]]
}
let output = try JSONSerialization.data(withJSONObject:["file":imagePath,"width":cg.width,"height":cg.height,"records":result], options:[.prettyPrinted,.sortedKeys])
FileHandle.standardOutput.write(output)

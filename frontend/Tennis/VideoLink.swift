//
//  VideoLink.swift
//  Tennis
//
//  Created by AndrewC on 12/2/21.
//

import Foundation

struct VideoLinkResponse: Codable {
    var success: Bool
    var data: String
}

struct VideoLinksResponse: Codable {
    var success: Bool
    var data: [String]
}

struct VideoUploadResponse: Codable {
    var success: Bool
    var data: String
}

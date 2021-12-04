import Alamofire
import Foundation
import AVKit

class NetworkManager {
    
    static let host = "https://tennis-trainer.herokuapp.com"
    
    static func getVideoLinkById(id: Int, completion: @escaping (String) -> Void) {
        AF.request("\(host)/api/media/\(id)", method: .get).validate().responseData { response in
            switch response.result {
            case .success(let data):
                let jsonDecoder = JSONDecoder()
                if let videoLinkResponse = try? jsonDecoder.decode(VideoLinkResponse.self, from: data) {
                    let videoLink = videoLinkResponse.data
                    completion(videoLink)
                }
            case .failure(let error):
                print("Get Video Failure: \(error)")
            }
        }
    }

}

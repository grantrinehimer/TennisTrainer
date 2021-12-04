
import UIKit
import AVKit
import AVFoundation
import Alamofire
import GoogleSignIn

protocol UpdateGoogleProfileDelegate: class {
    func updateGoogleUserID(id: String)
}

class PushViewController: UIViewController, UIImagePickerControllerDelegate & UINavigationControllerDelegate {
    weak var delegate: UpdateTitleDelegate?

    var userID = "";
    
    private var textFieldName = UITextField()
    private var textViewName = UITextView()
    
    private var textFieldDate = UITextField()
    private var textViewDate = UITextView()
    
    private var textFieldLink = UITextField()
    private var textViewLink = UITextView()
    
    private var saveButton = UIButton()
    
    private var placeholderTextName: String?
    private var placeholderTextDate: String?
    private var placeholderTextLink: String?
    
    private var currBucket: Bucket?
    private var indexPath: IndexPath?
    
    private var uploadButton = UIButton()
    private var playButton = UIButton()
    
    
    init(delegate: UpdateTitleDelegate?, bucket: Bucket, indexPath: IndexPath, placeholderTextName: String, placeholderTextDate: String, placeholderTextLink: String) {
        self.delegate = delegate
        self.currBucket = bucket
        self.indexPath = indexPath
        self.placeholderTextName = placeholderTextName
        self.placeholderTextDate = placeholderTextDate
        self.placeholderTextLink = placeholderTextLink
        super.init(nibName: nil, bundle: nil)
    }
    
    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()

        view.backgroundColor = .white
        
        textFieldName.translatesAutoresizingMaskIntoConstraints = false
        textFieldName.font = UIFont.systemFont(ofSize: 18)
        textFieldName.text = placeholderTextName
        textFieldName.borderStyle = .roundedRect
        textFieldName.textAlignment = .center
        view.addSubview(textFieldName)
        
        
        textViewName.translatesAutoresizingMaskIntoConstraints = false
        textViewName.font = UIFont.systemFont(ofSize: 18)
        textViewName.text = "Bucket Name"
        textViewName.textAlignment = .left
        view.addSubview(textViewName)
        
        textFieldDate.translatesAutoresizingMaskIntoConstraints = false
        textFieldDate.font = UIFont.systemFont(ofSize: 18)
        textFieldDate.text = placeholderTextDate
        textFieldDate.borderStyle = .roundedRect
        textFieldDate.textAlignment = .center
        view.addSubview(textFieldDate)
        
        
        textViewDate.translatesAutoresizingMaskIntoConstraints = false
        textViewDate.font = UIFont.systemFont(ofSize: 18)
        textViewDate.text = "Today's Date"
        textViewDate.textAlignment = .left
        view.addSubview(textViewDate)
        



        playButton.translatesAutoresizingMaskIntoConstraints = false
        playButton.setTitle("11/20/2021", for: .normal)
        playButton.setTitleColor(.black, for: .normal)
        playButton.backgroundColor = UIColor(red: 200/255, green: 200/255, blue: 200/255, alpha: 1)
        playButton.layer.cornerRadius = 4
        playButton.addTarget(self, action: #selector(playVideo), for: .touchUpInside)
        view.addSubview(playButton)
        
        
        uploadButton.translatesAutoresizingMaskIntoConstraints = false
        uploadButton.setTitle("Upload", for: .normal)
        uploadButton.setTitleColor(.black, for: .normal)
        uploadButton.backgroundColor = UIColor(red: 200/255, green: 200/255, blue: 200/255, alpha: 1)
        uploadButton.layer.cornerRadius = 4
        uploadButton.addTarget(self, action: #selector(selectImageFromPhotoLibrary), for: .touchUpInside)
        view.addSubview(uploadButton)
        
        
        
        saveButton.translatesAutoresizingMaskIntoConstraints = false
        saveButton.setTitle("Save", for: .normal)
        saveButton.setTitleColor(.black, for: .normal)
        saveButton.backgroundColor = UIColor(red: 200/255, green: 200/255, blue: 200/255, alpha: 1)
        saveButton.layer.cornerRadius = 4
        saveButton.addTarget(self, action: #selector(saveInfo), for: .touchUpInside)
        view.addSubview(saveButton)
        
        setUpConstraints()

    }
    
    
    
    
    func setUpConstraints() {
        
        NSLayoutConstraint.activate([
            textViewName.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            textViewName.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor, constant: 20),
            textViewName.widthAnchor.constraint(equalTo: view.widthAnchor, constant: -24),
            textViewName.heightAnchor.constraint(equalToConstant: 32)
        ])
        
        NSLayoutConstraint.activate([
            textFieldName.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            textFieldName.topAnchor.constraint(equalTo: textViewName.bottomAnchor, constant: 10),
            textFieldName.widthAnchor.constraint(equalTo: view.widthAnchor, constant: -24),
            textFieldName.heightAnchor.constraint(equalToConstant: 32)
        ])
        
        NSLayoutConstraint.activate([
            textViewDate.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            textViewDate.topAnchor.constraint(equalTo: textFieldName.bottomAnchor, constant: 20),
            textViewDate.widthAnchor.constraint(equalTo: view.widthAnchor, constant: -24),
            textViewDate.heightAnchor.constraint(equalToConstant: 32)
        ])
        
        NSLayoutConstraint.activate([
            textFieldDate.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            textFieldDate.topAnchor.constraint(equalTo: textViewDate.bottomAnchor, constant: 10),
            textFieldDate.widthAnchor.constraint(equalTo: view.widthAnchor, constant: -24),
            textFieldDate.heightAnchor.constraint(equalToConstant: 32)
        ])
        
        NSLayoutConstraint.activate([
            saveButton.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            saveButton.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor, constant: 5),
            saveButton.widthAnchor.constraint(equalToConstant: 120),
            saveButton.heightAnchor.constraint(equalToConstant: 32)
        ])

        NSLayoutConstraint.activate([
            uploadButton.widthAnchor.constraint(equalToConstant: 120),
            uploadButton.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            uploadButton.heightAnchor.constraint(equalToConstant: 32),
            uploadButton.topAnchor.constraint(equalTo: textFieldDate.bottomAnchor, constant: 20)
        ])
        
        NSLayoutConstraint.activate([
            playButton.widthAnchor.constraint(equalToConstant: 120),
            playButton.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            playButton.heightAnchor.constraint(equalToConstant: 32),
            playButton.topAnchor.constraint(equalTo: uploadButton.bottomAnchor, constant: 20)
        ])
        
    }
    
    let imagePickerController = UIImagePickerController()
    var videoURL: NSURL?

    @IBAction func selectImageFromPhotoLibrary(sender: UIBarButtonItem) {
      self.imagePickerController.sourceType = .photoLibrary
      self.imagePickerController.delegate = self
      self.imagePickerController.mediaTypes = ["public.image", "public.movie"]

      present(self.imagePickerController, animated: true, completion: nil)
      //print("hello")
    }
    
    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]) {
            dismiss(animated: true, completion: nil)
            //guard let movieUrl = info[.mediaURL] as? NSURL
            //print(movieUrl)

        if let videoUrl = info[.mediaURL] as? URL {

            let headers: HTTPHeaders = [
                "Content-type": "multipart/form-data"
            ]

         AF.upload(
            multipartFormData: { (multipartFormData) in
                multipartFormData.append("sampleFileName".data(using: String.Encoding.utf8, allowLossyConversion: false)!, withName: "filename")
                multipartFormData.append("sampleDisplayTitle".data(using: String.Encoding.utf8, allowLossyConversion: false)!, withName: "display_title")
                multipartFormData.append(self.userID.data(using: String.Encoding.utf8, allowLossyConversion: false)!, withName: "uid")

                
                multipartFormData.append(videoUrl, withName: "file")
//             multipartFormData.append(videoUrl, withName: "file", fileName: "movie.mov", mimeType: "video/mov")

             }, to:"https://tennis-trainer.herokuapp.com/api/media/", method: .post , headers: headers)
             { (result) in
                 print(result.debugDescription)

             }
            



//         self.dismiss(animated: true, completion: nil)
         }
    }
    
    func imagePickerControllerDidCancel(_ picker: UIImagePickerController) {
            dismiss(animated: true, completion: nil)
    }
    
    @IBAction func playVideo(_ sender: UIButton) {
        guard let url = URL(string: "https://appdev-backend-final.s3.us-east-2.amazonaws.com/hls/example.fmp4/index.m3u8") else { return }

        // Create an AVPlayer, passing it the HTTP Live Streaming URL.
        let player = AVPlayer(url: url)

        // Create a new AVPlayerViewController and pass it a reference to the player.
        let controller = AVPlayerViewController()
        controller.player = player

        // Modally present the player and call the player's play() method when complete.
        present(controller, animated: true) {
            player.play()
        }
    }
    
    @objc func saveInfo() {
        delegate?.updateBucketInfo(bucket: currBucket ?? Bucket(name: "", date: "", link: "", bucketImage: ""), indexPath: indexPath ?? IndexPath(), name: textFieldName.text ?? "", date: textFieldDate.text ?? "", link: textFieldLink.text ?? "")
        
    }

}

extension PushViewController: UpdateGoogleProfileDelegate {

    func updateGoogleUserID(id: String) {
        userID = id
    }

}

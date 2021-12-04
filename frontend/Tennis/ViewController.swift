import UIKit
import AVKit
import AVFoundation
import GoogleSignIn
import CloudKit

protocol UpdateTitleDelegate: class {
    func updateBucketInfo(bucket: Bucket, indexPath: IndexPath, name: String, date: String, link: String)
}

class ViewController: UIViewController {
    weak var delegate: UpdateGoogleProfileDelegate?

    let signInConfig = GIDConfiguration.init(clientID: "353843950130-ltob99bnq2pukci7m1qckaotg74f07m9.apps.googleusercontent.com")
    var signedInStatus = UITextView()
    
    var tableView = UITableView()

    let reuseIdentifier = "bucketCellReuse"
    let cellHeight: CGFloat = 50
    
    var currBucket: Bucket?
    var buckets: [Bucket] = []
    
    private var playButton = UIButton()

    override func viewDidLoad() {
        super.viewDidLoad()
        title = "Uploads"
        view.backgroundColor = .white

        let bhg = Bucket(name: "Backhand Groundstroke", date: "11/20/2021", link: "https://www.youtube.com/watch?v=dQw4w9WgXcQ", bucketImage: "tennisBall")
        let fhg = Bucket(name: "Forehand Groundstroke", date: "11/20/2021", link: "https://www.youtube.com/watch?v=dQw4w9WgXcQ", bucketImage: "tennisBall")
        let bhv = Bucket(name: "Backhand Volley", date: "11/20/2021", link: "https://www.youtube.com/watch?v=dQw4w9WgXcQ", bucketImage: "tennisBall")
        let fhv = Bucket(name: "Forehand Volley", date: "11/20/2021", link: "https://www.youtube.com/watch?v=dQw4w9WgXcQ", bucketImage: "tennisBall")
        let serve = Bucket(name: "Serve", date: "11/20/2021", link: "https://www.youtube.com/watch?v=dQw4w9WgXcQ", bucketImage: "tennisBall")
        buckets = [bhg, fhg, bhv, fhv, serve]
        
        tableView.translatesAutoresizingMaskIntoConstraints = false
        tableView.dataSource = self
        tableView.delegate = self
        tableView.register(bucketTableViewCell.self, forCellReuseIdentifier: reuseIdentifier)
        view.addSubview(tableView)
        
        playButton.translatesAutoresizingMaskIntoConstraints = false
        playButton.setTitle("Sign In", for: .normal)
        playButton.setTitleColor(.black, for: .normal)
        playButton.backgroundColor = UIColor(red: 200/255, green: 200/255, blue: 200/255, alpha: 1)
        playButton.layer.cornerRadius = 4
        playButton.addTarget(self, action: #selector(signIn), for: .touchUpInside)
        view.addSubview(playButton)
        
        signedInStatus.translatesAutoresizingMaskIntoConstraints = false
        signedInStatus.font = UIFont.systemFont(ofSize: 18)
        signedInStatus.text = "Not Signed In"
        signedInStatus.textAlignment = .left
        view.addSubview(signedInStatus)

        setupConstraints()
    }

    func setupConstraints() {
        NSLayoutConstraint.activate([
            tableView.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            tableView.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            tableView.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor),
            tableView.bottomAnchor.constraint(equalTo: view.safeAreaLayoutGuide.bottomAnchor)
        ])
        NSLayoutConstraint.activate([
            playButton.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            playButton.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            playButton.heightAnchor.constraint(equalToConstant: 20),
            playButton.bottomAnchor.constraint(equalTo: view.safeAreaLayoutGuide.bottomAnchor)
        ])
        NSLayoutConstraint.activate([
            signedInStatus.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            signedInStatus.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            signedInStatus.heightAnchor.constraint(equalToConstant: 40),
            signedInStatus.bottomAnchor.constraint(equalTo: playButton.topAnchor, constant: -20)
        ])
    }
    
    @IBAction func playVideo(_ sender: UIButton) {
        guard let url = URL(string: "https://appdev-backend-final.s3.us-east-2.amazonaws.com/hls/RFvsNadal_full_point_0.fmp4/index.m3u8") else { return }

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
    
    @IBAction func signIn(sender: Any) {
      GIDSignIn.sharedInstance.signIn(with: signInConfig, presenting: self) { user, error in
          guard error == nil else { return }
          guard let user = user else { return }
          
          let emailAddress = user.profile?.email

          let fullName = user.profile?.name
          let givenName = user.profile?.givenName
          let familyName = user.profile?.familyName
          let profilePicUrl = user.profile?.imageURL(withDimension: 320)

          if let uUserID = user.userID {
              self.delegate?.updateGoogleUserID(id: uUserID)
          } else {
              print("Failed unwrapping of UserID")
          }
          
          if let uFullName = fullName {
              self.signedInStatus.text = "Hello, \(uFullName)!"
          } else {
              self.signedInStatus.text = "Hello! You're signed in."
          }
          self.playButton.setTitle("Sign In to a Different Account", for: .normal)
          
          user.authentication.do { authentication, error in
              guard error == nil else { return }
              guard let authentication = authentication else { return }

              let idToken = authentication.idToken
              if let uIdToken = idToken {
                  self.tokenSignInExample(idToken: uIdToken)
              } else {
                  print("Authentication Failed")
              }
              
          }
          
      }
    }
    
    func tokenSignInExample(idToken: String) {
        guard let authData = try? JSONEncoder().encode(["token": idToken]) else {
            return
        }
        let url = URL(string: "https://tennis-trainer.herokuapp.com/api/user/authenticate/")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let task = URLSession.shared.uploadTask(with: request, from: authData) { data, response, error in
            print(response)
        }
        task.resume()
    }
    @IBAction func signOut(sender: Any) {
      GIDSignIn.sharedInstance.signOut()
        self.signedInStatus.text = "Not Signed In"
        self.playButton.setTitle("Sign In", for: .normal)
    }
}



extension ViewController: UITableViewDataSource {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return buckets.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        if let cell = tableView.dequeueReusableCell(withIdentifier: reuseIdentifier, for: indexPath) as? bucketTableViewCell {
            let bucket = buckets[indexPath.row]
            cell.configure(bucket: bucket)
            cell.selectionStyle = .none
            return cell
        } else {
            return UITableViewCell()
        }
    }
    
    
}

extension ViewController: UITableViewDelegate {
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        return 50
    }
    
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        let bucket = buckets[indexPath.row]
        currBucket = bucket
        let vc = PushViewController(delegate: self, bucket: bucket, indexPath: indexPath, placeholderTextName: bucket.name, placeholderTextDate: bucket.date, placeholderTextLink: bucket.link)
        navigationController?.pushViewController(vc, animated: true)
        
        
    }
}

extension ViewController: UpdateTitleDelegate {

    func updateBucketInfo(bucket: Bucket, indexPath: IndexPath, name: String, date: String, link: String) {
        buckets[indexPath.row].name = name
        buckets[indexPath.row].date = date
        buckets[indexPath.row].link = link
        tableView.reloadData()
    }

}


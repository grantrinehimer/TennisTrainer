import UIKit

protocol UpdateTitleDelegate: class {
    func updateBucketInfo(bucket: Bucket, indexPath: IndexPath, name: String, date: String, link: String)
}

class ViewController: UIViewController {

    var tableView = UITableView()

    let reuseIdentifier = "bucketCellReuse"
    let cellHeight: CGFloat = 50
    
    var currBucket: Bucket?
    var buckets: [Bucket] = []

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

        setupConstraints()
    }

    func setupConstraints() {
        NSLayoutConstraint.activate([
            tableView.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            tableView.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            tableView.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor),
            tableView.bottomAnchor.constraint(equalTo: view.safeAreaLayoutGuide.bottomAnchor)
        ])
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

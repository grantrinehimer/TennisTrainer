
import UIKit

class PushViewController: UIViewController {
    weak var delegate: UpdateTitleDelegate?

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
        
        textFieldLink.translatesAutoresizingMaskIntoConstraints = false
        textFieldLink.font = UIFont.systemFont(ofSize: 18)
        textFieldLink.text = placeholderTextLink
        textFieldLink.borderStyle = .roundedRect
        textFieldLink.textAlignment = .center
        view.addSubview(textFieldLink)
        
        
        textViewLink.translatesAutoresizingMaskIntoConstraints = false
        textViewLink.font = UIFont.systemFont(ofSize: 18)
        textViewLink.text = "Link (Youtube)"
        textViewLink.textAlignment = .left
        view.addSubview(textViewLink)
        
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
            saveButton.bottomAnchor.constraint(equalTo: view.bottomAnchor, constant: -12),
            saveButton.widthAnchor.constraint(equalToConstant: 120),
            saveButton.heightAnchor.constraint(equalToConstant: 32)
        ])
        
        NSLayoutConstraint.activate([
            textViewLink.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            textViewLink.topAnchor.constraint(equalTo: textFieldDate.bottomAnchor, constant: 20),
            textViewLink.widthAnchor.constraint(equalTo: view.widthAnchor, constant: -24),
            textViewLink.heightAnchor.constraint(equalToConstant: 32)
        ])
        
        NSLayoutConstraint.activate([
            textFieldLink.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            textFieldLink.topAnchor.constraint(equalTo: textViewLink.bottomAnchor, constant: 10),
            textFieldLink.widthAnchor.constraint(equalTo: view.widthAnchor, constant: -24),
            textFieldLink.heightAnchor.constraint(equalToConstant: 32)
        ])
        


    }
    
    @objc func saveInfo() {
        delegate?.updateBucketInfo(bucket: currBucket ?? Bucket(name: "", date: "", link: "", bucketImage: ""), indexPath: indexPath ?? IndexPath(), name: textFieldName.text ?? "", date: textFieldDate.text ?? "", link: textFieldLink.text ?? "")
        
    }

}


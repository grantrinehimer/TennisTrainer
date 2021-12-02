import UIKit

class bucketTableViewCell: UITableViewCell {

    var nameLabel = UILabel()
    var dateLabel = UILabel()
    var linkLabel = UILabel()
    var bucketImageView = UIImageView()

    override init(style: UITableViewCell.CellStyle, reuseIdentifier: String?) {
        super.init(style: style, reuseIdentifier: reuseIdentifier)

        nameLabel.font = .systemFont(ofSize: 14)
        nameLabel.translatesAutoresizingMaskIntoConstraints = false
        contentView.addSubview(nameLabel)

        dateLabel.font = .systemFont(ofSize: 12)
        dateLabel.translatesAutoresizingMaskIntoConstraints = false
        contentView.addSubview(dateLabel)
        
        linkLabel.font = .systemFont(ofSize: 12)
        linkLabel.translatesAutoresizingMaskIntoConstraints = false
        contentView.addSubview(linkLabel)

        bucketImageView.contentMode = .scaleAspectFit
        bucketImageView.translatesAutoresizingMaskIntoConstraints = false
        contentView.addSubview(bucketImageView)

        setupConstraints()
    }

    func configure(bucket: Bucket) {
        nameLabel.text = bucket.name
        dateLabel.text = "Last Updated: \(bucket.date)"
        //linkLabel.text = "Link: \(bucket.link)"
        bucketImageView.image = UIImage(named: bucket.bucketImage)
    }

    func setupConstraints() {
        let padding: CGFloat = 4
        let labelHeight: CGFloat = 15

        NSLayoutConstraint.activate([
            nameLabel.leadingAnchor.constraint(equalTo: contentView.leadingAnchor, constant: padding),
            nameLabel.topAnchor.constraint(equalTo: contentView.topAnchor, constant: padding),
            nameLabel.heightAnchor.constraint(equalToConstant: labelHeight)
        ])
        NSLayoutConstraint.activate([
            dateLabel.leadingAnchor.constraint(equalTo: nameLabel.leadingAnchor),
            dateLabel.topAnchor.constraint(equalTo: nameLabel.bottomAnchor),
            dateLabel.heightAnchor.constraint(equalToConstant: labelHeight)
        ])
        /*
        NSLayoutConstraint.activate([
            linkLabel.leadingAnchor.constraint(equalTo: nameLabel.leadingAnchor),
            linkLabel.topAnchor.constraint(equalTo: dateLabel.bottomAnchor),
            linkLabel.heightAnchor.constraint(equalToConstant: labelHeight)
        ])
 */
        NSLayoutConstraint.activate([
            bucketImageView.heightAnchor.constraint(equalToConstant: 40),
            bucketImageView.widthAnchor.constraint(equalToConstant: 40),
            bucketImageView.centerYAnchor.constraint(equalTo: contentView.centerYAnchor),
            bucketImageView.trailingAnchor.constraint(equalTo: contentView.trailingAnchor, constant: -padding)
        ])
    }

    func toggleHeart(isFavorite: Bool) {
        bucketImageView.isHidden = !isFavorite
    }

    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }

}

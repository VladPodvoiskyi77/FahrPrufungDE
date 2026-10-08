import Foundation

enum AppLinks {
    static let developerEmail = "appentwickler2025@gmail.com"
    static let mailtoURL = URL(string: "mailto:\(developerEmail)")!

    static let privacyPolicyURL: URL? = URL(
        string: "https://eclectic-concha-6a3c68.netlify.app/privacy-policy.html"
    )

    static let prapoDeAppStoreURL = URL(
        string: "https://apps.apple.com/app/id6758207550"
    )!
}

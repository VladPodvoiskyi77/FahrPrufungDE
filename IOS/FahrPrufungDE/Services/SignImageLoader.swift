import UIKit

enum SignImageLoader {
    private static let cache: NSCache<NSString, UIImage> = {
        let cache = NSCache<NSString, UIImage>()
        cache.countLimit = 256
        return cache
    }()

    static func image(for sign: TrafficSign) -> UIImage? {
        let cacheKey = sign.id as NSString
        if let cached = cache.object(forKey: cacheKey) {
            return cached
        }
        guard let path = sign.image, !path.isEmpty else { return nil }
        guard let image = image(relativePath: path) else { return nil }
        cache.setObject(image, forKey: cacheKey)
        return image
    }

    static func image(relativePath: String) -> UIImage? {
        let nsPath = relativePath as NSString
        let filename = nsPath.lastPathComponent
        let name = (filename as NSString).deletingPathExtension
        let ext = (filename as NSString).pathExtension.isEmpty ? "png" : (filename as NSString).pathExtension
        let subfolder = nsPath.deletingLastPathComponent

        if !subfolder.isEmpty {
            if let url = Bundle.main.url(
                forResource: name,
                withExtension: ext,
                subdirectory: "Signs/\(subfolder)"
            ) {
                return UIImage(contentsOfFile: url.path)
            }
        }

        if let url = Bundle.main.url(forResource: name, withExtension: ext, subdirectory: "Signs") {
            return UIImage(contentsOfFile: url.path)
        }

        return nil
    }
}

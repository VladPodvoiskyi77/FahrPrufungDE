import AVFoundation
import Combine

@MainActor
final class GermanSpeechService: NSObject, ObservableObject {
    static let shared = GermanSpeechService()

    @Published private(set) var speakingID: String?

    private let synthesizer = AVSpeechSynthesizer()
    private var delegateBridge: DelegateBridge?

    private override init() {
        super.init()
        let bridge = DelegateBridge { [weak self] in
            self?.speakingID = nil
        }
        delegateBridge = bridge
        synthesizer.delegate = bridge
    }

    func speakGerman(_ text: String, id: String) {
        let trimmed = text.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !trimmed.isEmpty else { return }

        if speakingID == id {
            stop()
            return
        }

        stop()
        speakingID = id

        let utterance = AVSpeechUtterance(string: trimmed)
        utterance.voice = AVSpeechSynthesisVoice(language: "de-DE")
        utterance.rate = AVSpeechUtteranceDefaultSpeechRate * 0.92
        synthesizer.speak(utterance)
    }

    func stop() {
        if synthesizer.isSpeaking {
            synthesizer.stopSpeaking(at: .immediate)
        }
        speakingID = nil
    }

    func isSpeaking(id: String) -> Bool {
        speakingID == id
    }

    private final class DelegateBridge: NSObject, AVSpeechSynthesizerDelegate {
        private let onFinish: () -> Void

        init(onFinish: @escaping () -> Void) {
            self.onFinish = onFinish
        }

        func speechSynthesizer(
            _ synthesizer: AVSpeechSynthesizer,
            didFinish utterance: AVSpeechUtterance
        ) {
            onFinish()
        }

        func speechSynthesizer(
            _ synthesizer: AVSpeechSynthesizer,
            didCancel utterance: AVSpeechUtterance
        ) {
            onFinish()
        }
    }
}

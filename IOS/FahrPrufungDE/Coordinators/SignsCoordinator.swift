import SwiftUI

enum SignsRoute: Hashable {
    case detail(TrafficSign)
}

@MainActor
final class SignsCoordinator: ObservableObject, FlowCoordinator {
    @Published var path = NavigationPath()

    func show(_ route: SignsRoute) {
        path.append(route)
    }

    func pop() {
        guard !path.isEmpty else { return }
        path.removeLast()
    }
}

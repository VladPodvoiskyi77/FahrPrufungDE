import SwiftUI

/// Root container: main UI loads underneath; splash fades out after 1.5 s.
struct RootView: View {
    @State private var showSplash = true

    var body: some View {
        ZStack {
            ContentView()

            if showSplash {
                SplashScreenView()
                    .transition(.opacity)
                    .zIndex(1)
            }
        }
        .onAppear {
            DispatchQueue.main.asyncAfter(deadline: .now() + 1.5) {
                withAnimation(.easeOut(duration: 0.35)) {
                    showSplash = false
                }
            }
        }
    }
}

struct SplashScreenView: View {
    @State private var appeared = false

    var body: some View {
        ZStack {
            AppTheme.heroGradient.ignoresSafeArea()

            VStack(spacing: 20) {
                Image("AppLogo")
                    .resizable()
                    .scaledToFit()
                    .frame(width: 120, height: 120)
                    .clipShape(RoundedRectangle(cornerRadius: 28, style: .continuous))
                    .shadow(color: .black.opacity(0.22), radius: 24, y: 12)

                Text(L10n.Home.title)
                    .font(AppTheme.titleFont(28))
                    .foregroundStyle(.white)
                    .multilineTextAlignment(.center)
            }
            .scaleEffect(appeared ? 1 : 0.88)
            .opacity(appeared ? 1 : 0)
        }
        .onAppear {
            withAnimation(AppMotion.spring) {
                appeared = true
            }
        }
    }
}

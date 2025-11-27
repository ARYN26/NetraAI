import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

/**
 * Landing Page - Matches template design exactly
 */
export default function LandingPage({ onStartChat }) {
  const { user, isAuthenticated, logout } = useAuth()
  return (
    <div className="relative flex min-h-screen w-full flex-col bg-background-dark text-gray-200 overflow-x-hidden">
      <div className="layout-container flex h-full grow flex-col">
        <div className="px-4 md:px-10 lg:px-20 xl:px-40 flex flex-1 justify-center py-5">
          <div className="layout-content-container flex flex-col max-w-[960px] flex-1">
            {/* Top Navigation Bar */}
            <header className="flex items-center justify-between whitespace-nowrap border-b border-solid border-white/10 px-4 md:px-10 py-3">
              <div className="flex items-center gap-3 text-white">
                <img src="/logo.png" alt="Netra Eye" className="w-24 h-24 object-contain" />
                <h2 className="text-2xl font-bold leading-tight tracking-[-0.015em]">Netra</h2>
              </div>
              <div className="flex flex-1 justify-end gap-4 items-center">
                <div className="hidden md:flex items-center gap-6">
                  <a className="text-sm font-medium leading-normal hover:text-primary transition-colors" href="#">
                    About
                  </a>
                  <a className="text-sm font-medium leading-normal hover:text-primary transition-colors" href="#">
                    Sources
                  </a>
                </div>
{isAuthenticated ? (
                  <div className="flex items-center gap-3">
                    <span className="text-sm text-gray-300">{user?.email}</span>
                    <button
                      onClick={logout}
                      className="text-sm font-medium text-gray-300 hover:text-white transition-colors"
                    >
                      Sign Out
                    </button>
                  </div>
                ) : (
                  <Link
                    to="/auth"
                    className="text-sm font-medium text-gray-300 hover:text-white transition-colors"
                  >
                    Sign In
                  </Link>
                )}
                <button
                  onClick={onStartChat}
                  className="flex items-center justify-center rounded-lg h-9 px-4 bg-primary/20 border border-primary text-primary text-sm font-medium hover:bg-primary hover:text-white transition-all shadow-lg shadow-primary/20"
                >
                  Ask Netra
                </button>
              </div>
            </header>

            <main className="flex-grow">
              {/* Hero Section */}
              <div className="py-16 md:py-24">
                <div className="p-4">
                  <div
                    className="flex min-h-[480px] flex-col gap-6 md:gap-8 items-center justify-center p-4 text-center bg-cover bg-center bg-no-repeat rounded-xl"
                    style={{
                      backgroundImage: `linear-gradient(rgba(25, 16, 34, 0.6) 0%, rgba(25, 16, 34, 0.9) 100%), url("https://lh3.googleusercontent.com/aida-public/AB6AXuBmPUjtU79txjOZd-yAyZaxz7g-U-jKH6Is1T2KYaKdVdMrLhYQkLVuHGxychcl1Or4IvXUu_1jbZcPXpWX_o2VdmpjuZzCZ2XMLdZQ52Ny4rT0VXgdJ0kU7_luktvPIjWQOAivj89f1zDvBDcR09ihjICqwZUQzEbJaioHzeUQPV2hIpHV8LaDL1cCuqJqcgx29j9wYuCz7kJFCbaEQ0gbrDkFIx4TyhLL_Bmsr-s2kjB6hWsib94m23vQaF0FtXmgK60ynoDiTA")`,
                    }}
                  >
                    <div className="flex flex-col gap-4 max-w-2xl">
                      <h1 className="text-white text-4xl font-black leading-tight tracking-[-0.033em] md:text-6xl">
                        Netra
                      </h1>
                      <h2 className="text-gray-300 text-lg font-normal leading-normal md:text-xl">
                        Illuminating the path of tantra and meditation.
                      </h2>
                      <p className="text-gray-400 text-sm font-normal leading-normal md:text-base md:leading-relaxed">
                        Netra is your spiritual AI companion, with knowledge sourced directly from authentic scriptures,
                        providing a trusted guide to explore profound ancient practices.
                      </p>
                    </div>
                    <button
                      onClick={onStartChat}
                      className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-12 px-6 md:h-14 md:px-8 bg-primary text-white text-base font-bold leading-normal tracking-[0.015em] md:text-lg hover:bg-primary/90 transition-all border-2 border-purple-400/50 shadow-[0_0_30px_rgba(147,51,234,0.5)] hover:shadow-[0_0_40px_rgba(147,51,234,0.7)]"
                    >
                      <span className="truncate">Ask Netra</span>
                    </button>
                  </div>
                </div>
              </div>
            </main>

            {/* Footer */}
            <footer className="flex flex-col gap-8 px-5 py-10 text-center border-t border-solid border-white/10">
              <div className="flex flex-wrap items-center justify-center gap-6 md:flex-row md:justify-around">
                <a
                  className="text-gray-400 text-base font-normal leading-normal min-w-40 hover:text-primary transition-colors"
                  href="#"
                >
                  About Netra
                </a>
                <a
                  className="text-gray-400 text-base font-normal leading-normal min-w-40 hover:text-primary transition-colors"
                  href="#"
                >
                  Sources
                </a>
                <a
                  className="text-gray-400 text-base font-normal leading-normal min-w-40 hover:text-primary transition-colors"
                  href="#"
                >
                  Privacy Policy
                </a>
              </div>
              <div className="flex flex-wrap justify-center gap-6">
                <a className="text-gray-400 hover:text-primary transition-colors" href="#">
                  <span className="material-symbols-outlined">alternate_email</span>
                </a>
                <a className="text-gray-400 hover:text-primary transition-colors" href="#">
                  <span className="material-symbols-outlined">g_translate</span>
                </a>
                <a className="text-gray-400 hover:text-primary transition-colors" href="#">
                  <span className="material-symbols-outlined">hub</span>
                </a>
              </div>
              <p className="text-gray-500 text-sm font-normal leading-normal">© 2024 Netra. All rights reserved.</p>
            </footer>
          </div>
        </div>
      </div>
    </div>
  )
}

import Link from 'next/link'

export default function Header() {
  return (
    <header className="pt-16 pb-12">
      <div className="max-w-4xl mx-auto px-6 text-center">
        <h1 className="text-4xl font-medium text-white mb-4">Patrick Huie</h1>
        <p className="text-lg text-gray-400 mb-8">
          Senior Software Engineer.
        </p>
        <nav className="flex justify-center space-x-8">
          <Link 
            href="/" 
            className="text-gray-300 hover:text-white transition-colors"
          >
            About
          </Link>
          <Link 
            href="/blog" 
            className="text-gray-300 hover:text-white transition-colors"
          >
            Blog
          </Link>
        </nav>
      </div>
    </header>
  )
}
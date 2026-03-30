import { getPostData, getAllPostIds } from '@/lib/posts'
import { notFound } from 'next/navigation'
import Link from 'next/link'
import { CopyMarkdown } from '@/components/CopyMarkdown'

export async function generateStaticParams() {
  const paths = getAllPostIds()
  return paths.map((path) => ({
    id: path.params.id,
  }))
}

export default async function Post({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  
  try {
    const postData = await getPostData(id)
    
    return (
      <div className="max-w-4xl mx-auto px-6 pb-16">
        <nav className="mb-8">
          <Link 
            href="/blog" 
            className="text-gray-400 hover:text-white transition-colors"
          >
            ← Back
          </Link>
        </nav>
        
        <article>
          <header className="mb-8">
            <h1 className="text-2xl font-medium text-white mb-2">{postData.title}</h1>
            <div className="flex items-center gap-3">
              <time className="text-gray-500 text-sm">
                {new Date(postData.date).toLocaleDateString('en-US', {
                  year: 'numeric',
                  month: 'short',
                  day: 'numeric',
                })}
              </time>
              <span className="text-gray-700">·</span>
              <CopyMarkdown text={postData.markdown} />
            </div>
          </header>
          
          <div 
            className="prose prose-invert max-w-none overflow-x-auto text-gray-300"
            dangerouslySetInnerHTML={{ __html: postData.content }}
          />
        </article>
      </div>
    )
  } catch {
    notFound()
  }
}
import Link from 'next/link'
import { getSortedPostsData } from '@/lib/posts'

export default function Blog() {
  const allPostsData = getSortedPostsData()

  return (
    <div className="max-w-4xl mx-auto px-6 pb-16">
      {allPostsData.length === 0 ? (
        <p className="text-gray-400 text-center">No posts yet.</p>
      ) : (
        <div className="space-y-8">
          {allPostsData.map(({ id, date, title, description }) => (
            <article key={id}>
              <Link href={`/blog/${id}`} className="block group">
                <div className="flex justify-between items-start mb-2">
                  <h2 className="text-white font-medium group-hover:text-gray-300 transition-colors">
                    {title}
                  </h2>
                  <time className="text-gray-500 text-sm">
                    {new Date(date).toLocaleDateString('en-US', {
                      year: 'numeric',
                      month: 'short',
                      day: 'numeric',
                    })}
                  </time>
                </div>
                {description && (
                  <p className="text-gray-400 text-sm">
                    {description}
                  </p>
                )}
              </Link>
            </article>
          ))}
        </div>
      )}
    </div>
  )
}
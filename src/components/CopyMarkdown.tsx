'use client'

import { useState, useCallback } from 'react'

export function CopyMarkdown({ text }: { text: string }) {
  const [copied, setCopied] = useState(false)

  const copy = useCallback(() => {
    navigator.clipboard.writeText(text).then(() => {
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    })
  }, [text])

  return (
    <button
      onClick={copy}
      className="text-gray-500 hover:text-gray-300 transition-colors text-sm cursor-pointer"
      aria-label="Copy post as markdown"
    >
      {copied ? 'Copied!' : 'Copy markdown'}
    </button>
  )
}

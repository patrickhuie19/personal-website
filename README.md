# Patrick Huie - Personal Website

A clean, minimal personal website built with Next.js, featuring an integrated blog system. Designed with a philosophy of building software for people - emphasizing openness, accessibility, reliability, and seamless user experiences.

This site was heavily built with AI.

## Features

- **Clean, Modern Design**: Dark theme with warm amber accents, avoiding navy blue
- **Responsive Layout**: Works perfectly on mobile and desktop
- **Static Site Generation**: Optimized for performance and easy hosting
- **Markdown Blog**: Simple blog system using markdown files
- **Accessibility**: Built with semantic HTML and proper contrast ratios

## Tech Stack

- **Framework**: Next.js 15 with App Router
- **Styling**: Tailwind CSS
- **Content**: Markdown with gray-matter and remark
- **Deployment**: Vercel-ready with static export

## Getting Started

### Development

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the site.

### Build

```bash
npm run build
```

Generates a static export in the `out/` directory.

### Adding Blog Posts

Create markdown files in the `posts/` directory:

```markdown
---
title: "Your Post Title"
date: "2025-01-15"
description: "Brief description of your post"
---

# Your content here

Write your blog post in markdown format.
```

## Project Structure

```
├── src/
│   ├── app/
│   │   ├── blog/
│   │   │   ├── [id]/
│   │   │   │   └── page.tsx    # Individual blog post pages
│   │   │   └── page.tsx        # Blog listing page
│   │   ├── globals.css         # Global styles
│   │   ├── layout.tsx          # Root layout
│   │   └── page.tsx            # Home page
│   ├── components/
│   │   ├── Header.tsx          # Navigation header
│   │   └── TrustVisualization.tsx  # Interactive demo
│   └── lib/
│       └── posts.ts            # Blog post utilities
├── posts/
│   └── *.md                    # Blog post files
└── public/                     # Static assets
```

## Deployment

### Vercel

This site is optimized for Vercel deployment:

1. Push your code to GitHub
2. Connect your repository to Vercel
3. Deploy automatically

### Other Static Hosts

The site exports to static files and can be hosted on:
- Netlify
- GitHub Pages
- AWS S3 + CloudFront
- Any static hosting service

## Philosophy

This website embodies the principle that good software should be invisible - it just works, providing value without drawing attention to itself. The design prioritizes:

- **User Experience**: Clean, intuitive navigation
- **Performance**: Fast loading times with static generation  
- **Accessibility**: Semantic markup and keyboard navigation
- **Reliability**: Simple architecture that's easy to maintain
- **Transparency**: Open source and well-documented

# Deployment Guide

This guide will help you deploy your Next.js website to your GoDaddy domain using Vercel (recommended) or alternative hosting options.

## Option 1: Deploy to Vercel (Recommended) ⭐

Vercel is made by the creators of Next.js and offers free hosting with automatic deployments.

### Step 1: Prepare Your Code

1. **Make sure your code is in a Git repository:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Push to GitHub:**
   - Create a new repository on GitHub
   - Push your code:
     ```bash
     git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
     git branch -M main
     git push -u origin main
     ```

### Step 2: Deploy to Vercel

1. **Sign up/Login to Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Sign up with your GitHub account (free)

2. **Import Your Project:**
   - Click "Add New Project"
   - Import your GitHub repository
   - Vercel will auto-detect Next.js settings
   - Click "Deploy"

3. **Your site is now live!** 
   - Vercel will give you a URL like: `your-site.vercel.app`

### Step 3: Connect Your GoDaddy Domain

1. **In Vercel Dashboard:**
   - Go to your project → Settings → Domains
   - Add your GoDaddy domain (e.g., `yourdomain.com` and `www.yourdomain.com`)

2. **Configure DNS in GoDaddy:**
   - Log into your GoDaddy account
   - Go to "My Products" → "DNS" (or "Domains" → "DNS")
   - You'll need to add these DNS records:

   **For the root domain (yourdomain.com):**
   - Type: `A`
   - Name: `@`
   - Value: `76.76.21.21` (Vercel's IP - check Vercel dashboard for current IP)
   - TTL: 600 (or default)

   **For www subdomain (www.yourdomain.com):**
   - Type: `CNAME`
   - Name: `www`
   - Value: `cname.vercel-dns.com`
   - TTL: 600 (or default)

3. **Wait for DNS Propagation:**
   - DNS changes can take 24-48 hours to propagate
   - Vercel will automatically detect when DNS is configured correctly
   - You can check status in Vercel dashboard

### Step 4: SSL Certificate (Automatic)

- Vercel automatically provides free SSL certificates
- Your site will be available at `https://yourdomain.com` once DNS propagates

---

## Troubleshooting

### DNS Not Working?
- Wait 24-48 hours for DNS propagation
- Use [whatsmydns.net](https://www.whatsmydns.net) to check DNS propagation
- Make sure you removed any conflicting DNS records

### Build Errors?
- Make sure all dependencies are in `package.json`
- Run `npm run build` locally to test
- Check Vercel build logs for specific errors

### Images Not Showing?
- Make sure images are in `public/` directory
- Use absolute paths like `/assets/image.png` (not `./assets/image.png`)

---

## Quick Reference

**Vercel Dashboard:** https://vercel.com/dashboard
**GoDaddy DNS:** https://www.godaddy.com/en-us/help/manage-dns-records-680
**Vercel DNS Docs:** https://vercel.com/docs/concepts/projects/domains

---

## Need Help?

- Check Vercel's documentation: https://vercel.com/docs
- GoDaddy support: https://www.godaddy.com/help
- Next.js deployment: https://nextjs.org/docs/deployment


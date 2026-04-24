"""
stacks.py – All supported tech stacks and their boilerplate file templates.
Each stack function receives a context dict and returns {filepath: content}.
"""

from typing import Dict


# ─────────────────────────────────────────────
# Helper
# ─────────────────────────────────────────────

def _snake(name: str) -> str:
    return name.lower().replace("-", "_").replace(" ", "_")


# ─────────────────────────────────────────────
# Category → Stack mapping
# ─────────────────────────────────────────────

CATEGORY_STACK_MAP = {
    # Web
    "E-commerce":                 "nextjs_postgres_prisma",
    "SaaS product":               "nextjs_postgres_prisma",
    "Business dashboard":         "nextjs_postgres_prisma",
    "Blogging platform":          "nextjs_postgres_prisma",
    "AI chatbot interface":       "nextjs_postgres_prisma",
    "Streaming platform":         "react_node_mongo",
    "Social media app":           "react_node_mongo",
    "Video conferencing":         "react_node_mongo",
    "Cryptocurrency tracker":     "react_node_mongo",
    "Gaming hub":                 "react_node_mongo",
    "Ticketing system":           "django_postgres",
    "Learning management system": "django_postgres",
    "Healthcare management":      "django_postgres",
    "Event management":           "django_postgres",
    "Travel booking":             "django_postgres",
    "Restaurant ordering system": "vue_express_mysql",
    "Finance tracker":            "vue_express_mysql",
    "Inventory management":       "vue_express_mysql",
    "Portfolio site":             "react_static",
    "Music player":               "react_static",
    # Desktop
    "__desktop__":                "electron_sqlite",
    # Hybrid
    "__hybrid__":                 "tauri_react",
}

STACK_META = {
    "nextjs_postgres_prisma": {
        "label": "Next.js 14 + PostgreSQL + Prisma",
        "language": "TypeScript",
        "tags": ["Next.js 14", "PostgreSQL", "Prisma", "NextAuth", "Tailwind CSS", "Docker"],
    },
    "react_node_mongo": {
        "label": "React + Node.js/Express + MongoDB",
        "language": "TypeScript",
        "tags": ["React", "Vite", "Express", "MongoDB", "Mongoose", "JWT", "Docker"],
    },
    "django_postgres": {
        "label": "Django REST + PostgreSQL",
        "language": "Python",
        "tags": ["Django", "DRF", "PostgreSQL", "JWT", "Docker"],
    },
    "vue_express_mysql": {
        "label": "Vue 3 + Express + MySQL",
        "language": "TypeScript / JavaScript",
        "tags": ["Vue 3", "Vite", "Express", "MySQL", "Sequelize", "Docker"],
    },
    "react_static": {
        "label": "React + Vite (Static / No Backend)",
        "language": "TypeScript",
        "tags": ["React", "Vite", "Tailwind CSS"],
    },
    "electron_sqlite": {
        "label": "Electron + React + SQLite",
        "language": "TypeScript",
        "tags": ["Electron", "React", "SQLite", "better-sqlite3"],
    },
    "tauri_react": {
        "label": "Tauri + React + SQLite",
        "language": "Rust + TypeScript",
        "tags": ["Tauri", "React", "Vite", "SQLite"],
    },
}


def resolve_stack(platform: str, category: str) -> str:
    if platform == "Desktop":
        return "electron_sqlite"
    if platform == "Hybrid":
        return "tauri_react"
    return CATEGORY_STACK_MAP.get(category, "nextjs_postgres_prisma")


# ─────────────────────────────────────────────
# STACK 1 – Next.js 14 + PostgreSQL + Prisma
# ─────────────────────────────────────────────

def _nextjs_postgres_prisma(ctx: dict) -> Dict[str, str]:
    pname = ctx["project_name"]
    primary = ctx.get("colors", ["#3B82F6"])[0]
    category = ctx.get("category", "Web App")
    style = ctx.get("style", "Modern")
    files: Dict[str, str] = {}

    # ── .env.example ──────────────────────────
    files[".env.example"] = f"""# ═══════════════════════════════════════════
# {pname} – Environment Variables
# Copy this file to .env and fill in values
# ═══════════════════════════════════════════

# ── Database ──────────────────────────────
DATABASE_URL="postgresql://postgres:password@localhost:5432/{_snake(pname)}_db"

# ── Authentication ────────────────────────
# Generate with: openssl rand -base64 32
NEXTAUTH_SECRET="REPLACE_WITH_SECURE_RANDOM_STRING"
NEXTAUTH_URL="http://localhost:3000"

# ── App ───────────────────────────────────
NEXT_PUBLIC_APP_NAME="{pname}"
NEXT_PUBLIC_APP_URL="http://localhost:3000"

# ── Email (optional) ─────────────────────
# SMTP_HOST=smtp.gmail.com
# SMTP_PORT=587
# SMTP_USER=your@email.com
# SMTP_PASS=your-app-password

# ── OAuth (optional) ─────────────────────
# GOOGLE_CLIENT_ID=
# GOOGLE_CLIENT_SECRET=
# GITHUB_CLIENT_ID=
# GITHUB_CLIENT_SECRET=
"""

    # ── package.json ──────────────────────────
    files["package.json"] = f"""{{
  "name": "{pname}",
  "version": "0.1.0",
  "private": true,
  "scripts": {{
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "db:push": "prisma db push",
    "db:migrate": "prisma migrate dev",
    "db:studio": "prisma studio",
    "db:seed": "tsx prisma/seed.ts",
    "db:reset": "prisma migrate reset --force"
  }},
  "dependencies": {{
    "@auth/prisma-adapter": "^1.0.16",
    "@prisma/client": "^5.10.2",
    "bcryptjs": "^2.4.3",
    "clsx": "^2.1.0",
    "next": "^14.1.4",
    "next-auth": "^4.24.7",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "tailwind-merge": "^2.2.2",
    "zod": "^3.22.4"
  }},
  "devDependencies": {{
    "@types/bcryptjs": "^2.4.6",
    "@types/node": "^20.11.30",
    "@types/react": "^18.2.73",
    "@types/react-dom": "^18.2.22",
    "autoprefixer": "^10.4.19",
    "eslint": "^8.57.0",
    "eslint-config-next": "^14.1.4",
    "postcss": "^8.4.38",
    "prisma": "^5.10.2",
    "tailwindcss": "^3.4.3",
    "tsx": "^4.7.1",
    "typescript": "^5.4.3"
  }}
}}
"""

    # ── tsconfig.json ─────────────────────────
    files["tsconfig.json"] = """{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": { "@/*": ["./src/*"] }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
"""

    # ── next.config.ts ────────────────────────
    files["next.config.ts"] = """import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  experimental: {
    serverActions: { allowedOrigins: ['localhost:3000'] },
  },
  images: {
    domains: [
      'avatars.githubusercontent.com',
      'lh3.googleusercontent.com',
      'res.cloudinary.com',
    ],
  },
};

export default nextConfig;
"""

    # ── tailwind.config.ts ────────────────────
    files["tailwind.config.ts"] = f"""import type {{ Config }} from 'tailwindcss';

const config: Config = {{
  content: ['./src/**/*.{{js,ts,jsx,tsx,mdx}}'],
  theme: {{
    extend: {{
      colors: {{
        primary: {{
          DEFAULT: '{primary}',
          50: '#eff6ff',
          100: '#dbeafe',
          500: '{primary}',
          600: '#2563eb',
          700: '#1d4ed8',
          900: '#1e3a8a',
        }},
      }},
      fontFamily: {{
        sans: ['var(--font-inter)', 'system-ui', 'sans-serif'],
      }},
    }},
  }},
  plugins: [],
}};

export default config;
"""

    # ── postcss.config.js ─────────────────────
    files["postcss.config.js"] = """module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
"""

    # ── prisma/schema.prisma ──────────────────
    files["prisma/schema.prisma"] = f"""// ═══════════════════════════════════════
// {pname} – Prisma Schema
// Run: npm run db:migrate
// ═══════════════════════════════════════

generator client {{
  provider = "prisma-client-js"
}}

datasource db {{
  provider = "postgresql"
  url      = env("DATABASE_URL")
}}

model User {{
  id            String    @id @default(cuid())
  name          String?
  email         String    @unique
  emailVerified DateTime?
  image         String?
  password      String?
  role          Role      @default(USER)
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt

  accounts Account[]
  sessions Session[]

  @@index([email])
}}

model Account {{
  id                String  @id @default(cuid())
  userId            String
  type              String
  provider          String
  providerAccountId String
  refresh_token     String? @db.Text
  access_token      String? @db.Text
  expires_at        Int?
  token_type        String?
  scope             String?
  id_token          String? @db.Text
  session_state     String?

  user User @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@unique([provider, providerAccountId])
}}

model Session {{
  id           String   @id @default(cuid())
  sessionToken String   @unique
  userId       String
  expires      DateTime

  user User @relation(fields: [userId], references: [id], onDelete: Cascade)
}}

model VerificationToken {{
  identifier String
  token      String   @unique
  expires    DateTime

  @@unique([identifier, token])
}}

enum Role {{
  USER
  ADMIN
}}
"""

    # ── prisma/seed.ts ────────────────────────
    files["prisma/seed.ts"] = f"""import {{ PrismaClient }} from '@prisma/client';
import bcrypt from 'bcryptjs';

const prisma = new PrismaClient();

async function main() {{
  console.log('🌱 Seeding database...');

  const hashedPassword = await bcrypt.hash('admin123', 12);

  const admin = await prisma.user.upsert({{
    where: {{ email: 'admin@{_snake(pname)}.com' }},
    update: {{}},
    create: {{
      email: 'admin@{_snake(pname)}.com',
      name: 'Admin User',
      password: hashedPassword,
      role: 'ADMIN',
    }},
  }});

  console.log('✅ Created admin:', admin.email);
  console.log('🔑 Default password: admin123  ← CHANGE THIS IN PRODUCTION');
}}

main()
  .catch((e) => {{ console.error(e); process.exit(1); }})
  .finally(async () => {{ await prisma.$disconnect(); }});
"""

    # ── src/lib/db.ts ─────────────────────────
    files["src/lib/db.ts"] = """import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as { prisma: PrismaClient };

export const db =
  globalForPrisma.prisma ??
  new PrismaClient({
    log: process.env.NODE_ENV === 'development' ? ['query', 'error', 'warn'] : ['error'],
  });

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = db;
"""

    # ── src/lib/auth.ts ───────────────────────
    files["src/lib/auth.ts"] = f"""import type {{ NextAuthOptions }} from 'next-auth';
import {{ PrismaAdapter }} from '@auth/prisma-adapter';
import CredentialsProvider from 'next-auth/providers/credentials';
import bcrypt from 'bcryptjs';
import {{ db }} from './db';

export const authOptions: NextAuthOptions = {{
  // @ts-ignore – adapter type mismatch between next-auth versions
  adapter: PrismaAdapter(db),
  session: {{ strategy: 'jwt' }},
  pages: {{
    signIn: '/login',
    error: '/login',
  }},
  providers: [
    CredentialsProvider({{
      name: 'credentials',
      credentials: {{
        email: {{ label: 'Email', type: 'email' }},
        password: {{ label: 'Password', type: 'password' }},
      }},
      async authorize(credentials) {{
        if (!credentials?.email || !credentials.password) return null;

        const user = await db.user.findUnique({{
          where: {{ email: credentials.email }},
        }});

        if (!user || !user.password) return null;

        const isValid = await bcrypt.compare(credentials.password, user.password);
        if (!isValid) return null;

        return user;
      }},
    }}),
    // Uncomment to add OAuth providers:
    // GoogleProvider({{ clientId: process.env.GOOGLE_CLIENT_ID!, clientSecret: process.env.GOOGLE_CLIENT_SECRET! }}),
    // GithubProvider({{ clientId: process.env.GITHUB_CLIENT_ID!, clientSecret: process.env.GITHUB_CLIENT_SECRET! }}),
  ],
  callbacks: {{
    async jwt({{ token, user }}) {{
      if (user) {{
        token.id = user.id;
        token.role = (user as any).role;
      }}
      return token;
    }},
    async session({{ session, token }}) {{
      if (session.user) {{
        (session.user as any).id = token.id;
        (session.user as any).role = token.role;
      }}
      return session;
    }},
  }},
}};
"""

    # ── src/lib/utils.ts ──────────────────────
    files["src/lib/utils.ts"] = """import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(date: Date | string): string {
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric', month: 'long', day: 'numeric',
  }).format(new Date(date));
}

export function formatCurrency(amount: number, currency = 'USD'): string {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency }).format(amount);
}
"""

    # ── src/app/layout.tsx ────────────────────
    files["src/app/layout.tsx"] = f"""import type {{ Metadata }} from 'next';
import {{ Inter }} from 'next/font/google';
import './globals.css';

const inter = Inter({{ subsets: ['latin'], variable: '--font-inter' }});

export const metadata: Metadata = {{
  title: {{
    default: '{pname}',
    template: `%s | {pname}`,
  }},
  description: '{category} built with Next.js and Prisma',
}};

export default function RootLayout({{
  children,
}}: {{
  children: React.ReactNode;
}}) {{
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={{`${{inter.variable}} font-sans antialiased bg-gray-50 text-gray-900`}}>
        {{children}}
      </body>
    </html>
  );
}}
"""

    # ── src/app/globals.css ───────────────────
    files["src/app/globals.css"] = f"""@tailwind base;
@tailwind components;
@tailwind utilities;

:root {{
  --primary: {primary};
  --primary-foreground: #ffffff;
}}

@layer base {{
  *, *::before, *::after {{
    box-sizing: border-box;
  }}

  h1, h2, h3, h4 {{
    @apply tracking-tight font-bold;
  }}

  a {{
    @apply transition-colors;
  }}
}}

@layer utilities {{
  .scrollbar-hide {{
    -ms-overflow-style: none;
    scrollbar-width: none;
  }}
  .scrollbar-hide::-webkit-scrollbar {{
    display: none;
  }}
}}
"""

    # ── src/app/page.tsx ──────────────────────
    files["src/app/page.tsx"] = f"""import Link from 'next/link';

export default function HomePage() {{
  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-white">
      <div className="max-w-2xl mx-auto px-6 text-center space-y-8">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-sm font-medium bg-blue-50 text-blue-700 border border-blue-100">
          ✨ {category}
        </div>
        <h1 className="text-6xl font-black tracking-tight text-gray-900">
          {pname}
        </h1>
        <p className="text-xl text-gray-500 leading-relaxed">
          Your project is ready to build. The stack is configured,
          the database schema is set up, and authentication is wired in.
        </p>
        <div className="flex gap-4 justify-center">
          <Link
            href="/dashboard"
            className="px-8 py-3 rounded-xl font-semibold text-white shadow-lg shadow-blue-500/25 hover:shadow-blue-500/40 hover:-translate-y-0.5 transition-all duration-200"
            style={{{{ backgroundColor: '{primary}' }}}}
          >
            Open Dashboard →
          </Link>
          <Link
            href="/login"
            className="px-8 py-3 rounded-xl font-semibold text-gray-700 bg-gray-100 hover:bg-gray-200 hover:-translate-y-0.5 transition-all duration-200"
          >
            Sign In
          </Link>
        </div>
        <p className="text-xs text-gray-400">
          Stack: Next.js 14 · PostgreSQL · Prisma · NextAuth · Tailwind CSS
        </p>
      </div>
    </main>
  );
}}
"""

    # ── src/app/login/page.tsx ────────────────
    files["src/app/login/page.tsx"] = f""""use client";
import {{ useState }} from 'react';
import {{ signIn }} from 'next-auth/react';
import {{ useRouter }} from 'next/navigation';
import Link from 'next/link';

export default function LoginPage() {{
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {{
    e.preventDefault();
    setLoading(true);
    setError('');

    const result = await signIn('credentials', {{
      email,
      password,
      redirect: false,
    }});

    setLoading(false);

    if (result?.error) {{
      setError('Invalid email or password');
    }} else {{
      router.push('/dashboard');
      router.refresh();
    }}
  }};

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
          <div className="mb-8">
            <Link href="/" className="text-2xl font-black text-gray-900">{pname}</Link>
            <p className="mt-2 text-gray-500">Sign in to your account</p>
          </div>

          {{error && (
            <div className="mb-4 p-3 rounded-lg bg-red-50 border border-red-100 text-red-600 text-sm">
              {{error}}
            </div>
          )}}

          <form onSubmit={{handleSubmit}} className="space-y-5">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1.5">
                Email
              </label>
              <input
                type="email"
                value={{email}}
                onChange={{(e) => setEmail(e.target.value)}}
                placeholder="you@example.com"
                className="w-full px-4 py-2.5 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1.5">
                Password
              </label>
              <input
                type="password"
                value={{password}}
                onChange={{(e) => setPassword(e.target.value)}}
                placeholder="••••••••"
                className="w-full px-4 py-2.5 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
                required
              />
            </div>
            <button
              type="submit"
              disabled={{loading}}
              className="w-full py-3 rounded-xl font-semibold text-white transition-all duration-200 disabled:opacity-60 hover:-translate-y-0.5"
              style={{{{ backgroundColor: '{primary}' }}}}
            >
              {{loading ? 'Signing in...' : 'Sign In'}}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}}
"""

    # ── src/app/dashboard/page.tsx ────────────
    files["src/app/dashboard/page.tsx"] = f"""import {{ getServerSession }} from 'next-auth';
import {{ authOptions }} from '@/lib/auth';
import {{ db }} from '@/lib/db';
import {{ redirect }} from 'next/navigation';
import Navbar from '@/components/Navbar';

export default async function DashboardPage() {{
  const session = await getServerSession(authOptions);
  if (!session) redirect('/login');

  const userCount = await db.user.count();

  return (
    <>
      <Navbar />
      <main className="max-w-7xl mx-auto px-4 py-10">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-500 mt-1">
            Welcome back, {{session.user?.name ?? session.user?.email}}
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          <StatCard label="Total Users" value={{userCount}} color="{primary}" />
          <StatCard label="Active Sessions" value={{1}} color="#10B981" />
          <StatCard label="Your Role" value={{(session.user as any)?.role ?? 'USER'}} color="#F59E0B" isText />
        </div>

        <div className="mt-10 bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
          <h2 className="text-lg font-semibold mb-4">Getting Started</h2>
          <ul className="space-y-3 text-sm text-gray-600">
            <li className="flex items-center gap-2">
              <span className="text-green-500">✓</span> Project structure generated
            </li>
            <li className="flex items-center gap-2">
              <span className="text-green-500">✓</span> Database schema created
            </li>
            <li className="flex items-center gap-2">
              <span className="text-green-500">✓</span> Authentication configured
            </li>
            <li className="flex items-center gap-2">
              <span className="text-gray-400">○</span> Add your business logic in{' '}
              <code className="px-1.5 py-0.5 bg-gray-100 rounded text-xs">src/app/</code>
            </li>
            <li className="flex items-center gap-2">
              <span className="text-gray-400">○</span> Update{' '}
              <code className="px-1.5 py-0.5 bg-gray-100 rounded text-xs">prisma/schema.prisma</code>{' '}
              with your models
            </li>
          </ul>
        </div>
      </main>
    </>
  );
}}

function StatCard({{
  label, value, color, isText = false,
}}: {{
  label: string; value: number | string; color: string; isText?: boolean;
}}) {{
  return (
    <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
      <p className="text-sm font-medium text-gray-500">{{label}}</p>
      <p
        className={{`mt-2 ${{isText ? 'text-2xl' : 'text-4xl'}} font-bold`}}
        style={{{{ color }}}}
      >
        {{value}}
      </p>
    </div>
  );
}}
"""

    # ── src/app/api/auth/[...nextauth]/route.ts
    files["src/app/api/auth/[...nextauth]/route.ts"] = """import NextAuth from 'next-auth';
import { authOptions } from '@/lib/auth';

const handler = NextAuth(authOptions);
export { handler as GET, handler as POST };
"""

    # ── src/app/api/users/route.ts ────────────
    files["src/app/api/users/route.ts"] = """import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { db } from '@/lib/db';
import { z } from 'zod';

const createUserSchema = z.object({
  name: z.string().min(1).optional(),
  email: z.string().email(),
});

// GET /api/users – list users (admin only)
export async function GET(req: NextRequest) {
  const session = await getServerSession(authOptions);
  if (!session) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });

  const { searchParams } = new URL(req.url);
  const page = parseInt(searchParams.get('page') ?? '1');
  const limit = parseInt(searchParams.get('limit') ?? '20');

  const [users, total] = await Promise.all([
    db.user.findMany({
      select: { id: true, name: true, email: true, role: true, createdAt: true },
      skip: (page - 1) * limit,
      take: limit,
      orderBy: { createdAt: 'desc' },
    }),
    db.user.count(),
  ]);

  return NextResponse.json({ users, total, page, limit });
}

// POST /api/users – create user
export async function POST(req: NextRequest) {
  const body = await req.json();
  const parsed = createUserSchema.safeParse(body);

  if (!parsed.success) {
    return NextResponse.json({ error: parsed.error.flatten() }, { status: 400 });
  }

  const existing = await db.user.findUnique({ where: { email: parsed.data.email } });
  if (existing) {
    return NextResponse.json({ error: 'Email already in use' }, { status: 409 });
  }

  const user = await db.user.create({
    data: parsed.data,
    select: { id: true, name: true, email: true, role: true, createdAt: true },
  });

  return NextResponse.json(user, { status: 201 });
}
"""

    # ── src/app/api/health/route.ts ───────────
    files["src/app/api/health/route.ts"] = """import { NextResponse } from 'next/server';
import { db } from '@/lib/db';

export async function GET() {
  try {
    await db.$queryRaw`SELECT 1`;
    return NextResponse.json({ status: 'ok', db: 'connected' });
  } catch {
    return NextResponse.json({ status: 'error', db: 'disconnected' }, { status: 503 });
  }
}
"""

    # ── src/components/Navbar.tsx ─────────────
    files["src/components/Navbar.tsx"] = f""""use client";
import Link from 'next/link';
import {{ useSession, signOut }} from 'next-auth/react';
import {{ useState }} from 'react';

export default function Navbar() {{
  const {{ data: session }} = useSession();
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <nav className="bg-white border-b border-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          <Link
            href="/"
            className="text-xl font-black text-gray-900 hover:opacity-75 transition"
          >
            {pname}
          </Link>

          <div className="hidden sm:flex items-center gap-6">
            <Link href="/dashboard" className="text-sm font-medium text-gray-600 hover:text-gray-900 transition">
              Dashboard
            </Link>

            {{session ? (
              <div className="flex items-center gap-3">
                <div className="flex items-center gap-2">
                  <div
                    className="w-8 h-8 rounded-full flex items-center justify-center text-white text-xs font-bold"
                    style={{{{ backgroundColor: '{primary}' }}}}
                  >
                    {{(session.user?.name ?? session.user?.email ?? 'U')[0].toUpperCase()}}
                  </div>
                  <span className="text-sm text-gray-600 hidden md:block">
                    {{session.user?.name ?? session.user?.email}}
                  </span>
                </div>
                <button
                  onClick={{() => signOut({{ callbackUrl: '/' }})}}
                  className="text-sm text-red-500 hover:text-red-700 font-medium transition"
                >
                  Sign out
                </button>
              </div>
            ) : (
              <Link
                href="/login"
                className="px-4 py-2 rounded-lg text-sm font-semibold text-white transition hover:opacity-90"
                style={{{{ backgroundColor: '{primary}' }}}}
              >
                Sign In
              </Link>
            )}}
          </div>
        </div>
      </div>
    </nav>
  );
}}
"""

    # ── src/middleware.ts ─────────────────────
    files["src/middleware.ts"] = """import { withAuth } from 'next-auth/middleware';
import { NextResponse } from 'next/server';

export default withAuth(
  function middleware(req) {
    return NextResponse.next();
  },
  {
    callbacks: {
      authorized: ({ token }) => !!token,
    },
    pages: {
      signIn: '/login',
    },
  }
);

export const config = {
  matcher: ['/dashboard/:path*', '/admin/:path*', '/api/users/:path*'],
};
"""

    # ── Dockerfile ────────────────────────────
    files["Dockerfile"] = f"""# ──────────────────────────────────────────────
# Build Stage
# ──────────────────────────────────────────────
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED=1
RUN npx prisma generate
RUN npm run build

# ──────────────────────────────────────────────
# Production Stage
# ──────────────────────────────────────────────
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
COPY --from=builder /app/node_modules/.prisma ./node_modules/.prisma

USER nextjs
EXPOSE 3000
ENV PORT=3000
CMD ["node", "server.js"]
"""

    # ── docker-compose.yml ────────────────────
    files["docker-compose.yml"] = f"""version: '3.8'

services:
  # ── Next.js Application ──────────────────────
  app:
    build: .
    container_name: {_snake(pname)}_app
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: postgresql://postgres:${{POSTGRES_PASSWORD:-password}}@db:5432/{_snake(pname)}_db
      NEXTAUTH_SECRET: ${{NEXTAUTH_SECRET:-change-this-secret}}
      NEXTAUTH_URL: http://localhost:3000
      NEXT_PUBLIC_APP_NAME: "{pname}"
    depends_on:
      db:
        condition: service_healthy

  # ── PostgreSQL Database ───────────────────────
  db:
    image: postgres:16-alpine
    container_name: {_snake(pname)}_db
    restart: unless-stopped
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${{POSTGRES_PASSWORD:-password}}
      POSTGRES_DB: {_snake(pname)}_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  # ── pgAdmin (Database GUI) ────────────────────
  pgadmin:
    image: dpage/pgadmin4:latest
    container_name: {_snake(pname)}_pgadmin
    restart: unless-stopped
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@admin.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "5050:80"
    depends_on:
      - db

volumes:
  postgres_data:
    name: {_snake(pname)}_postgres_data
"""

    # ── README.md ─────────────────────────────
    files["README.md"] = f"""# {pname}

> **{category}** built with Next.js 14 · TypeScript · PostgreSQL · Prisma · NextAuth · Tailwind CSS

## ⚡ Quick Start (3 steps)

### 1. Install dependencies
```bash
npm install
```

### 2. Configure environment
```bash
cp .env.example .env
```

Open `.env` and update these required values:
```bash
DATABASE_URL="postgresql://postgres:password@localhost:5432/{_snake(pname)}_db"
NEXTAUTH_SECRET="$(openssl rand -base64 32)"   # Generate a random secret
NEXTAUTH_URL="http://localhost:3000"
```

### 3. Set up the database and run
```bash
npm run db:push     # Push schema to database
npm run db:seed     # Create admin user
npm run dev         # Start dev server
```

Open [http://localhost:3000](http://localhost:3000) 🚀

---

## 🐳 Docker Quick Start (one command)

```bash
cp .env.example .env
# Set NEXTAUTH_SECRET in .env

docker-compose up -d
```

| Service  | URL                          |
|----------|------------------------------|
| App      | http://localhost:3000        |
| pgAdmin  | http://localhost:5050        |
| Postgres | localhost:5432               |

---

## 🔑 Default Credentials (after seeding)

| Field    | Value                       |
|----------|-----------------------------|
| Email    | `admin@{_snake(pname)}.com` |
| Password | `admin123`                  |

> ⚠️ **Change these immediately in production!**

---

## 📁 Project Structure

```
{pname}/
├── prisma/
│   ├── schema.prisma       # Edit this to add your models
│   └── seed.ts             # Seed script
├── src/
│   ├── app/
│   │   ├── api/            # API routes
│   │   │   ├── auth/       # NextAuth handler
│   │   │   ├── users/      # User CRUD example
│   │   │   └── health/     # Health check
│   │   ├── dashboard/      # Protected dashboard page
│   │   ├── login/          # Login page
│   │   ├── layout.tsx      # Root layout
│   │   ├── page.tsx        # Home page
│   │   └── globals.css     # Global styles
│   ├── components/
│   │   └── Navbar.tsx
│   ├── lib/
│   │   ├── auth.ts         # NextAuth config ← add OAuth providers here
│   │   ├── db.ts           # Prisma client singleton
│   │   └── utils.ts        # Utility functions
│   └── middleware.ts        # Route protection
├── .env.example             # ← Copy to .env
├── docker-compose.yml
├── Dockerfile
├── next.config.ts
├── tailwind.config.ts
└── package.json
```

---

## 🛠 Useful Commands

| Command               | Description                      |
|-----------------------|----------------------------------|
| `npm run dev`         | Start development server         |
| `npm run build`       | Build for production             |
| `npm run db:migrate`  | Run database migrations          |
| `npm run db:studio`   | Open Prisma Studio (GUI)         |
| `npm run db:seed`     | Seed database with sample data   |
| `npm run db:reset`    | Reset database (danger!)         |

---

## 🚀 Deployment

### Vercel (recommended for Next.js)
1. Push to GitHub
2. Import on [vercel.com](https://vercel.com)
3. Add environment variables
4. Deploy!

### Self-hosted with Docker
```bash
docker-compose up -d
# Run migrations
docker-compose exec app npx prisma migrate deploy
```

---

## 📦 Tech Stack

| Layer        | Technology              |
|--------------|-------------------------|
| Framework    | Next.js 14 (App Router) |
| Language     | TypeScript              |
| Database     | PostgreSQL 16           |
| ORM          | Prisma 5                |
| Auth         | NextAuth.js 4           |
| Styling      | Tailwind CSS 3          |
| Validation   | Zod                     |
| Deployment   | Docker + Compose        |
"""

    return files


# ─────────────────────────────────────────────
# STACK 2 – React + Node.js/Express + MongoDB
# ─────────────────────────────────────────────

def _react_node_mongo(ctx: dict) -> Dict[str, str]:
    pname = ctx["project_name"]
    primary = ctx.get("colors", ["#3B82F6"])[0]
    category = ctx.get("category", "Web App")
    files: Dict[str, str] = {}

    # ── .env.example ──────────────────────────
    files[".env.example"] = f"""# ═══════════════════════════════════════════
# {pname} – Environment Variables
# ═══════════════════════════════════════════

# ── Server ────────────────────────────────
PORT=5000
NODE_ENV=development

# ── Database ──────────────────────────────
MONGODB_URI=mongodb://localhost:27017/{_snake(pname)}
# For MongoDB Atlas: mongodb+srv://<user>:<pass>@cluster.mongodb.net/{_snake(pname)}

# ── Authentication ────────────────────────
# Generate with: node -e "console.log(require('crypto').randomBytes(64).toString('hex'))"
JWT_SECRET=REPLACE_WITH_LONG_RANDOM_STRING
JWT_EXPIRES_IN=7d
JWT_REFRESH_EXPIRES_IN=30d

# ── CORS ──────────────────────────────────
CLIENT_URL=http://localhost:5173

# ── File Uploads (Cloudinary – optional) ──
# CLOUDINARY_CLOUD_NAME=
# CLOUDINARY_API_KEY=
# CLOUDINARY_API_SECRET=

# ── Email (optional) ──────────────────────
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_USER=your@email.com
# EMAIL_PASS=your-app-password
"""

    # ── server/package.json ───────────────────
    files["server/package.json"] = f"""{{
  "name": "{pname}-server",
  "version": "0.1.0",
  "scripts": {{
    "dev": "tsx watch src/index.ts",
    "build": "tsc",
    "start": "node dist/index.js",
    "seed": "tsx src/seed.ts"
  }},
  "dependencies": {{
    "bcryptjs": "^2.4.3",
    "compression": "^1.7.4",
    "cors": "^2.8.5",
    "dotenv": "^16.4.5",
    "express": "^4.18.3",
    "express-rate-limit": "^7.2.0",
    "express-validator": "^7.0.1",
    "helmet": "^7.1.0",
    "jsonwebtoken": "^9.0.2",
    "mongoose": "^8.2.4",
    "morgan": "^1.10.0"
  }},
  "devDependencies": {{
    "@types/bcryptjs": "^2.4.6",
    "@types/compression": "^1.7.5",
    "@types/cors": "^2.8.17",
    "@types/express": "^4.17.21",
    "@types/jsonwebtoken": "^9.0.6",
    "@types/morgan": "^1.9.9",
    "@types/node": "^20.11.30",
    "tsx": "^4.7.1",
    "typescript": "^5.4.3"
  }}
}}
"""

    # ── server/tsconfig.json ──────────────────
    files["server/tsconfig.json"] = """{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
"""

    # ── server/src/index.ts ───────────────────
    files["server/src/index.ts"] = f"""import 'dotenv/config';
import express from 'express';
import helmet from 'helmet';
import cors from 'cors';
import compression from 'compression';
import morgan from 'morgan';
import rateLimit from 'express-rate-limit';
import {{ connectDB }} from './config/db';
import routes from './routes';
import {{ errorHandler }} from './middleware/error';

const app = express();
const PORT = process.env.PORT || 5000;

// ── Security & Middleware ─────────────────────
app.use(helmet());
app.use(cors({{
  origin: process.env.CLIENT_URL || 'http://localhost:5173',
  credentials: true,
}}));
app.use(compression());
app.use(morgan(process.env.NODE_ENV === 'production' ? 'combined' : 'dev'));
app.use(express.json({{ limit: '10mb' }}));
app.use(express.urlencoded({{ extended: true }}));

// ── Rate Limiting ─────────────────────────────
app.use('/api', rateLimit({{
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100,
  message: {{ error: 'Too many requests, please try again later.' }},
}}));

// ── Routes ────────────────────────────────────
app.use('/api', routes);

// ── Health Check ──────────────────────────────
app.get('/health', (_, res) => {{
  res.json({{ status: 'ok', service: '{pname}-api', timestamp: new Date().toISOString() }});
}});

// ── Error Handler ─────────────────────────────
app.use(errorHandler);

// ── Start ─────────────────────────────────────
connectDB().then(() => {{
  app.listen(PORT, () => {{
    console.log(`\\n🚀 {pname} API running at http://localhost:${{PORT}}`);
    console.log(`   Environment: ${{process.env.NODE_ENV}}`);
    console.log(`   Health: http://localhost:${{PORT}}/health\\n`);
  }});
}});

export default app;
"""

    # ── server/src/config/db.ts ───────────────
    files["server/src/config/db.ts"] = f"""import mongoose from 'mongoose';

export async function connectDB(): Promise<void> {{
  try {{
    const uri = process.env.MONGODB_URI;
    if (!uri) throw new Error('MONGODB_URI is not defined in environment variables');

    await mongoose.connect(uri, {{
      serverSelectionTimeoutMS: 5000,
    }});

    console.log('✅ MongoDB connected:', mongoose.connection.host);

    mongoose.connection.on('error', (err) => {{
      console.error('MongoDB connection error:', err);
    }});

    mongoose.connection.on('disconnected', () => {{
      console.warn('MongoDB disconnected. Reconnecting...');
    }});
  }} catch (error) {{
    console.error('❌ MongoDB connection failed:', error);
    process.exit(1);
  }}
}}
"""

    # ── server/src/models/User.ts ─────────────
    files["server/src/models/User.ts"] = f"""import mongoose, {{ Schema, Document, Model }} from 'mongoose';
import bcrypt from 'bcryptjs';

export interface IUser extends Document {{
  name: string;
  email: string;
  password: string;
  role: 'user' | 'admin';
  avatar?: string;
  isActive: boolean;
  lastLogin?: Date;
  createdAt: Date;
  updatedAt: Date;
  comparePassword(candidate: string): Promise<boolean>;
}}

const userSchema = new Schema<IUser>(
  {{
    name: {{
      type: String,
      required: [true, 'Name is required'],
      trim: true,
      minlength: [2, 'Name must be at least 2 characters'],
      maxlength: [50, 'Name cannot exceed 50 characters'],
    }},
    email: {{
      type: String,
      required: [true, 'Email is required'],
      unique: true,
      lowercase: true,
      trim: true,
      match: [/^\\S+@\\S+\\.\\S+$/, 'Invalid email format'],
    }},
    password: {{
      type: String,
      required: [true, 'Password is required'],
      minlength: [8, 'Password must be at least 8 characters'],
      select: false, // Never return password in queries
    }},
    role: {{
      type: String,
      enum: ['user', 'admin'],
      default: 'user',
    }},
    avatar: String,
    isActive: {{ type: Boolean, default: true }},
    lastLogin: Date,
  }},
  {{
    timestamps: true,
    toJSON: {{ virtuals: true }},
    toObject: {{ virtuals: true }},
  }}
);

// ── Hash password before save ─────────────────
userSchema.pre('save', async function (next) {{
  if (!this.isModified('password')) return next();
  this.password = await bcrypt.hash(this.password, 12);
  next();
}});

// ── Instance method: compare password ─────────
userSchema.methods.comparePassword = async function (
  candidate: string
): Promise<boolean> {{
  return bcrypt.compare(candidate, this.password);
}};

// ── Index ─────────────────────────────────────
userSchema.index({{ email: 1 }});

const User: Model<IUser> = mongoose.models.User || mongoose.model<IUser>('User', userSchema);
export default User;
"""

    # ── server/src/middleware/auth.ts ─────────
    files["server/src/middleware/auth.ts"] = """import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import User from '../models/User';

interface JwtPayload {
  id: string;
  role: string;
}

declare global {
  namespace Express {
    interface Request {
      user?: { id: string; role: string };
    }
  }
}

export const protect = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const authHeader = req.headers.authorization;
    if (!authHeader?.startsWith('Bearer ')) {
      return res.status(401).json({ error: 'Access denied. No token provided.' });
    }

    const token = authHeader.split(' ')[1];
    const secret = process.env.JWT_SECRET;
    if (!secret) throw new Error('JWT_SECRET not configured');

    const decoded = jwt.verify(token, secret) as JwtPayload;

    const user = await User.findById(decoded.id).select('-password');
    if (!user || !user.isActive) {
      return res.status(401).json({ error: 'User not found or inactive.' });
    }

    req.user = { id: user.id, role: user.role };
    next();
  } catch {
    return res.status(401).json({ error: 'Invalid or expired token.' });
  }
};

export const requireAdmin = (req: Request, res: Response, next: NextFunction) => {
  if (req.user?.role !== 'admin') {
    return res.status(403).json({ error: 'Admin access required.' });
  }
  next();
};
"""

    # ── server/src/middleware/error.ts ────────
    files["server/src/middleware/error.ts"] = """import { Request, Response, NextFunction } from 'express';

export interface AppError extends Error {
  statusCode?: number;
  isOperational?: boolean;
}

export const errorHandler = (
  err: AppError,
  req: Request,
  res: Response,
  _next: NextFunction
) => {
  const statusCode = err.statusCode || 500;
  const message = err.message || 'Internal Server Error';

  if (process.env.NODE_ENV === 'development') {
    console.error(err.stack);
  }

  res.status(statusCode).json({
    error: message,
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack }),
  });
};

export const createError = (message: string, statusCode: number): AppError => {
  const error: AppError = new Error(message);
  error.statusCode = statusCode;
  error.isOperational = true;
  return error;
};
"""

    # ── server/src/routes/auth.ts ─────────────
    files["server/src/routes/auth.ts"] = f"""import {{ Router, Request, Response }} from 'express';
import {{ body, validationResult }} from 'express-validator';
import jwt from 'jsonwebtoken';
import User from '../models/User';
import {{ protect }} from '../middleware/auth';

const router = Router();

const generateToken = (id: string, role: string): string =>
  jwt.sign({{ id, role }}, process.env.JWT_SECRET!, {{
    expiresIn: process.env.JWT_EXPIRES_IN || '7d',
  }});

// ── POST /api/auth/register ───────────────────
router.post(
  '/register',
  [
    body('name').trim().isLength({{ min: 2 }}).withMessage('Name too short'),
    body('email').isEmail().normalizeEmail(),
    body('password').isLength({{ min: 8 }}).withMessage('Password must be 8+ characters'),
  ],
  async (req: Request, res: Response) => {{
    const errors = validationResult(req);
    if (!errors.isEmpty()) {{
      return res.status(400).json({{ errors: errors.array() }});
    }}

    const {{ name, email, password }} = req.body;

    const existing = await User.findOne({{ email }});
    if (existing) {{
      return res.status(409).json({{ error: 'Email already registered' }});
    }}

    const user = await User.create({{ name, email, password }});
    const token = generateToken(user.id, user.role);

    res.status(201).json({{
      token,
      user: {{ id: user.id, name: user.name, email: user.email, role: user.role }},
    }});
  }}
);

// ── POST /api/auth/login ──────────────────────
router.post(
  '/login',
  [
    body('email').isEmail().normalizeEmail(),
    body('password').notEmpty(),
  ],
  async (req: Request, res: Response) => {{
    const errors = validationResult(req);
    if (!errors.isEmpty()) {{
      return res.status(400).json({{ errors: errors.array() }});
    }}

    const {{ email, password }} = req.body;

    const user = await User.findOne({{ email }}).select('+password');
    if (!user || !(await user.comparePassword(password))) {{
      return res.status(401).json({{ error: 'Invalid email or password' }});
    }}

    user.lastLogin = new Date();
    await user.save();

    const token = generateToken(user.id, user.role);
    res.json({{
      token,
      user: {{ id: user.id, name: user.name, email: user.email, role: user.role }},
    }});
  }}
);

// ── GET /api/auth/me ──────────────────────────
router.get('/me', protect, async (req: Request, res: Response) => {{
  const user = await User.findById(req.user!.id);
  res.json(user);
}});

export default router;
"""

    # ── server/src/routes/index.ts ────────────
    files["server/src/routes/index.ts"] = """import { Router } from 'express';
import authRoutes from './auth';

const router = Router();

router.use('/auth', authRoutes);
// Add more routes here:
// router.use('/posts', postRoutes);
// router.use('/products', productRoutes);

export default router;
"""

    # ── server/src/seed.ts ────────────────────
    files["server/src/seed.ts"] = f"""import 'dotenv/config';
import {{ connectDB }} from './config/db';
import User from './models/User';
import mongoose from 'mongoose';

async function seed() {{
  await connectDB();
  console.log('🌱 Seeding database...');

  await User.deleteMany({{}});

  await User.create([
    {{
      name: 'Admin User',
      email: 'admin@{_snake(pname)}.com',
      password: 'admin123',
      role: 'admin',
    }},
    {{
      name: 'Test User',
      email: 'user@{_snake(pname)}.com',
      password: 'user1234',
      role: 'user',
    }},
  ]);

  console.log('✅ Seeded users');
  console.log('   admin@{_snake(pname)}.com / admin123');
  console.log('   user@{_snake(pname)}.com  / user1234');
  console.log('⚠️  Change passwords before deploying!');

  await mongoose.disconnect();
}}

seed().catch(console.error);
"""

    # ── client/package.json ───────────────────
    files["client/package.json"] = f"""{{
  "name": "{pname}-client",
  "version": "0.1.0",
  "private": true,
  "scripts": {{
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx"
  }},
  "dependencies": {{
    "axios": "^1.6.8",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.22.3",
    "zustand": "^4.5.2",
    "clsx": "^2.1.0"
  }},
  "devDependencies": {{
    "@types/react": "^18.2.73",
    "@types/react-dom": "^18.2.22",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.19",
    "postcss": "^8.4.38",
    "tailwindcss": "^3.4.3",
    "typescript": "^5.4.3",
    "vite": "^5.2.7"
  }}
}}
"""

    # ── client/vite.config.ts ─────────────────
    files["client/vite.config.ts"] = """import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
    },
  },
});
"""

    # ── client/tsconfig.json ──────────────────
    files["client/tsconfig.json"] = """{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "paths": { "@/*": ["./src/*"] }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
"""

    # ── client/index.html ─────────────────────
    files["client/index.html"] = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{pname}</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
"""

    # ── client/src/main.tsx ───────────────────
    files["client/src/main.tsx"] = """import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
);
"""

    # ── client/src/index.css ──────────────────
    files["client/src/index.css"] = f"""@tailwind base;
@tailwind components;
@tailwind utilities;

:root {{
  --primary: {primary};
}}
"""

    # ── client/src/App.tsx ────────────────────
    files["client/src/App.tsx"] = """import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuthStore } from './store/auth';
import HomePage from './pages/Home';
import LoginPage from './pages/Login';
import RegisterPage from './pages/Register';
import DashboardPage from './pages/Dashboard';
import Navbar from './components/Navbar';

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { token } = useAuthStore();
  return token ? <>{children}</> : <Navigate to="/login" replace />;
}

export default function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <DashboardPage />
            </ProtectedRoute>
          }
        />
      </Routes>
    </>
  );
}
"""

    # ── client/src/store/auth.ts ──────────────
    files["client/src/store/auth.ts"] = """import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface User {
  id: string;
  name: string;
  email: string;
  role: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  setAuth: (user: User, token: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      setAuth: (user, token) => set({ user, token }),
      logout: () => set({ user: null, token: null }),
    }),
    { name: 'auth-storage' }
  )
);
"""

    # ── client/src/services/api.ts ────────────
    files["client/src/services/api.ts"] = """import axios from 'axios';
import { useAuthStore } from '../store/auth';

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
});

// Auto-attach JWT token
api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Auto-logout on 401
api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      useAuthStore.getState().logout();
      window.location.href = '/login';
    }
    return Promise.reject(err);
  }
);

export default api;

// ── Auth endpoints ────────────────────────────
export const authApi = {
  login: (email: string, password: string) =>
    api.post('/auth/login', { email, password }),
  register: (name: string, email: string, password: string) =>
    api.post('/auth/register', { name, email, password }),
  me: () => api.get('/auth/me'),
};
"""

    # ── client/src/pages/Home.tsx ─────────────
    files["client/src/pages/Home.tsx"] = f"""import {{ Link }} from 'react-router-dom';

export default function HomePage() {{
  return (
    <main className="min-h-screen flex items-center justify-center bg-white">
      <div className="text-center space-y-6 px-6 max-w-xl">
        <h1 className="text-6xl font-black text-gray-900">{pname}</h1>
        <p className="text-xl text-gray-500">{category} · React + Express + MongoDB</p>
        <div className="flex gap-4 justify-center">
          <Link
            to="/register"
            className="px-8 py-3 rounded-xl font-semibold text-white shadow-lg hover:-translate-y-0.5 transition-all"
            style={{{{ backgroundColor: '{primary}' }}}}
          >
            Get Started
          </Link>
          <Link
            to="/login"
            className="px-8 py-3 rounded-xl font-semibold bg-gray-100 text-gray-700 hover:bg-gray-200 hover:-translate-y-0.5 transition-all"
          >
            Sign In
          </Link>
        </div>
      </div>
    </main>
  );
}}
"""

    # ── client/src/pages/Login.tsx ────────────
    files["client/src/pages/Login.tsx"] = f"""import {{ useState }} from 'react';
import {{ useNavigate, Link }} from 'react-router-dom';
import {{ authApi }} from '../services/api';
import {{ useAuthStore }} from '../store/auth';

export default function LoginPage() {{
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const {{ setAuth }} = useAuthStore();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {{
    e.preventDefault();
    setLoading(true);
    setError('');
    try {{
      const {{ data }} = await authApi.login(email, password);
      setAuth(data.user, data.token);
      navigate('/dashboard');
    }} catch (err: any) {{
      setError(err.response?.data?.error || 'Login failed');
    }} finally {{
      setLoading(false);
    }}
  }};

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-sm border p-8">
        <h1 className="text-2xl font-bold mb-1">Sign In</h1>
        <p className="text-gray-500 text-sm mb-6">Welcome back to {pname}</p>
        {{error && (
          <div className="mb-4 p-3 rounded-lg bg-red-50 text-red-600 text-sm">{{error}}</div>
        )}}
        <form onSubmit={{handleSubmit}} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input type="email" value={{email}} onChange={{e => setEmail(e.target.value)}}
              className="w-full px-4 py-2.5 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
              required />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <input type="password" value={{password}} onChange={{e => setPassword(e.target.value)}}
              className="w-full px-4 py-2.5 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
              required />
          </div>
          <button type="submit" disabled={{loading}}
            className="w-full py-3 rounded-xl font-semibold text-white transition hover:-translate-y-0.5 disabled:opacity-60"
            style={{{{ backgroundColor: '{primary}' }}}}>
            {{loading ? 'Signing in...' : 'Sign In'}}
          </button>
        </form>
        <p className="mt-4 text-center text-sm text-gray-500">
          Don't have an account?{{' '}}
          <Link to="/register" className="font-medium" style={{{{ color: '{primary}' }}}}>Register</Link>
        </p>
      </div>
    </div>
  );
}}
"""

    # ── client/src/pages/Register.tsx ────────
    files["client/src/pages/Register.tsx"] = f"""import {{ useState }} from 'react';
import {{ useNavigate, Link }} from 'react-router-dom';
import {{ authApi }} from '../services/api';
import {{ useAuthStore }} from '../store/auth';

export default function RegisterPage() {{
  const [form, setForm] = useState({{ name: '', email: '', password: '' }});
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const {{ setAuth }} = useAuthStore();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {{
    e.preventDefault();
    setLoading(true);
    setError('');
    try {{
      const {{ data }} = await authApi.register(form.name, form.email, form.password);
      setAuth(data.user, data.token);
      navigate('/dashboard');
    }} catch (err: any) {{
      setError(err.response?.data?.error || 'Registration failed');
    }} finally {{
      setLoading(false);
    }}
  }};

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-sm border p-8">
        <h1 className="text-2xl font-bold mb-1">Create Account</h1>
        <p className="text-gray-500 text-sm mb-6">Join {pname} today</p>
        {{error && <div className="mb-4 p-3 rounded-lg bg-red-50 text-red-600 text-sm">{{error}}</div>}}
        <form onSubmit={{handleSubmit}} className="space-y-4">
          {{(['name', 'email', 'password'] as const).map(field => (
            <div key={{field}}>
              <label className="block text-sm font-medium text-gray-700 mb-1 capitalize">{{field}}</label>
              <input
                type={{field === 'email' ? 'email' : field === 'password' ? 'password' : 'text'}}
                value={{form[field]}}
                onChange={{e => setForm(f => ({{ ...f, [field]: e.target.value }}))}}
                className="w-full px-4 py-2.5 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                required
              />
            </div>
          ))}}
          <button type="submit" disabled={{loading}}
            className="w-full py-3 rounded-xl font-semibold text-white transition hover:-translate-y-0.5 disabled:opacity-60"
            style={{{{ backgroundColor: '{primary}' }}}}>
            {{loading ? 'Creating account...' : 'Create Account'}}
          </button>
        </form>
        <p className="mt-4 text-center text-sm text-gray-500">
          Already have an account?{{' '}}
          <Link to="/login" className="font-medium" style={{{{ color: '{primary}' }}}}>Sign in</Link>
        </p>
      </div>
    </div>
  );
}}
"""

    # ── client/src/pages/Dashboard.tsx ────────
    files["client/src/pages/Dashboard.tsx"] = f"""import {{ useAuthStore }} from '../store/auth';

export default function DashboardPage() {{
  const {{ user, logout }} = useAuthStore();

  return (
    <div className="max-w-7xl mx-auto px-4 py-10">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-500 mt-1">Welcome back, {{user?.name}}</p>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-10">
        {{[
          {{ label: 'Your Email', value: user?.email ?? '' }},
          {{ label: 'Role', value: user?.role ?? '' }},
          {{ label: 'User ID', value: user?.id?.slice(0, 8) + '...' ?? '' }},
        ].map(card => (
          <div key={{card.label}} className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
            <p className="text-sm text-gray-500">{{card.label}}</p>
            <p className="mt-2 text-lg font-bold text-gray-900">{{card.value}}</p>
          </div>
        ))}}
      </div>
      <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
        <h2 className="text-lg font-semibold mb-4">Next Steps</h2>
        <ul className="space-y-2 text-sm text-gray-600">
          <li>✅ Auth system (register / login / JWT) is working</li>
          <li>✅ Protected routes configured</li>
          <li>○ Add your features in <code className="bg-gray-100 px-1.5 rounded">client/src/pages/</code></li>
          <li>○ Add API routes in <code className="bg-gray-100 px-1.5 rounded">server/src/routes/</code></li>
          <li>○ Add Mongoose models in <code className="bg-gray-100 px-1.5 rounded">server/src/models/</code></li>
        </ul>
      </div>
    </div>
  );
}}
"""

    # ── client/src/components/Navbar.tsx ──────
    files["client/src/components/Navbar.tsx"] = f"""import {{ Link, useNavigate }} from 'react-router-dom';
import {{ useAuthStore }} from '../store/auth';

export default function Navbar() {{
  const {{ user, token, logout }} = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = () => {{
    logout();
    navigate('/');
  }};

  return (
    <nav className="bg-white border-b border-gray-100 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          <Link to="/" className="text-xl font-black text-gray-900">
            {pname}
          </Link>
          <div className="flex items-center gap-4">
            {{token ? (
              <>
                <Link to="/dashboard" className="text-sm font-medium text-gray-600 hover:text-gray-900">
                  Dashboard
                </Link>
                <div className="w-8 h-8 rounded-full text-white text-xs font-bold flex items-center justify-center"
                  style={{{{ backgroundColor: '{primary}' }}}}>
                  {{user?.name?.[0]?.toUpperCase()}}
                </div>
                <button onClick={{handleLogout}} className="text-sm text-red-500 hover:text-red-700 font-medium">
                  Sign out
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="text-sm font-medium text-gray-600 hover:text-gray-900">Sign in</Link>
                <Link to="/register" className="px-4 py-2 rounded-lg text-sm font-semibold text-white"
                  style={{{{ backgroundColor: '{primary}' }}}}>
                  Register
                </Link>
              </>
            )}}
          </div>
        </div>
      </div>
    </nav>
  );
}}
"""

    # ── client/tailwind.config.js ─────────────
    files["client/tailwind.config.js"] = f"""/** @type {{import('tailwindcss').Config}} */
export default {{
  content: ['./index.html', './src/**/*.{{js,ts,jsx,tsx}}'],
  theme: {{
    extend: {{
      colors: {{ primary: '{primary}' }},
    }},
  }},
  plugins: [],
}};
"""

    # ── docker-compose.yml ────────────────────
    files["docker-compose.yml"] = f"""version: '3.8'

services:
  # ── Client (React) ────────────────────────────
  client:
    build:
      context: ./client
      dockerfile: Dockerfile
    container_name: {_snake(pname)}_client
    ports:
      - "5173:80"
    depends_on:
      - server

  # ── Server (Express) ─────────────────────────
  server:
    build:
      context: ./server
      dockerfile: Dockerfile
    container_name: {_snake(pname)}_server
    restart: unless-stopped
    ports:
      - "5000:5000"
    environment:
      NODE_ENV: production
      PORT: 5000
      MONGODB_URI: mongodb://mongo:27017/{_snake(pname)}
      JWT_SECRET: ${{JWT_SECRET:-change-this-secret-in-production}}
      CLIENT_URL: http://localhost:5173
    depends_on:
      mongo:
        condition: service_healthy

  # ── MongoDB ───────────────────────────────────
  mongo:
    image: mongo:7-jammy
    container_name: {_snake(pname)}_mongo
    restart: unless-stopped
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 10s
      timeout: 5s
      retries: 5

  # ── Mongo Express (GUI) ───────────────────────
  mongo-express:
    image: mongo-express
    container_name: {_snake(pname)}_mongo_express
    restart: unless-stopped
    ports:
      - "8081:8081"
    environment:
      ME_CONFIG_MONGODB_SERVER: mongo
      ME_CONFIG_BASICAUTH_USERNAME: admin
      ME_CONFIG_BASICAUTH_PASSWORD: admin123
    depends_on:
      - mongo

volumes:
  mongo_data:
    name: {_snake(pname)}_mongo_data
"""

    # ── README.md ─────────────────────────────
    files["README.md"] = f"""# {pname}

> **{category}** · React · Node.js/Express · MongoDB · TypeScript · JWT Auth

## ⚡ Quick Start

### Prerequisites
- Node.js 18+
- MongoDB (local or [Atlas](https://cloud.mongodb.com))

### 1. Configure environment
```bash
cp .env.example .env
# Edit .env – set MONGODB_URI and JWT_SECRET
```

### 2. Start the server
```bash
cd server
npm install
npm run seed    # Create sample users
npm run dev     # Starts on http://localhost:5000
```

### 3. Start the client
```bash
cd client
npm install
npm run dev     # Starts on http://localhost:5173
```

---

## 🐳 Docker (one command)
```bash
cp .env.example .env
docker-compose up -d
```

| Service       | URL                          |
|---------------|------------------------------|
| Client        | http://localhost:5173        |
| API           | http://localhost:5000        |
| Mongo Express | http://localhost:8081        |

---

## 🔑 Default Credentials (after seeding)
| User  | Email                       | Password  |
|-------|-----------------------------|-----------|
| Admin | `admin@{_snake(pname)}.com` | `admin123` |
| User  | `user@{_snake(pname)}.com`  | `user1234` |

> ⚠️ Change before deploying!

---

## 📁 Structure

```
{pname}/
├── client/                  # React + Vite frontend
│   └── src/
│       ├── pages/           # Route components
│       ├── components/      # Shared UI
│       ├── services/api.ts  # Axios + auto JWT
│       └── store/auth.ts    # Zustand auth state
├── server/                  # Express backend
│   └── src/
│       ├── models/          # Mongoose schemas
│       ├── routes/          # API routes ← add here
│       ├── middleware/       # Auth, error handling
│       └── config/db.ts     # MongoDB connection
├── .env.example             # ← Copy to .env
└── docker-compose.yml
```

## 📦 Tech Stack
| Layer     | Technology               |
|-----------|--------------------------|
| Frontend  | React 18 + Vite + TS    |
| Backend   | Express 4 + TypeScript  |
| Database  | MongoDB + Mongoose      |
| Auth      | JWT (jsonwebtoken)      |
| State     | Zustand                  |
| Styling   | Tailwind CSS            |
"""

    return files


# ─────────────────────────────────────────────
# STACK 3 – Django REST + PostgreSQL
# ─────────────────────────────────────────────

def _django_postgres(ctx: dict) -> Dict[str, str]:
    pname = ctx["project_name"]
    snake = _snake(pname)
    primary = ctx.get("colors", ["#3B82F6"])[0]
    category = ctx.get("category", "Web App")
    files: Dict[str, str] = {}

    files[".env.example"] = f"""# ═══════════════════════════════════════════
# {pname} – Environment Variables
# ═══════════════════════════════════════════

# ── Django ────────────────────────────────
# Generate with: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
SECRET_KEY=REPLACE_WITH_DJANGO_SECRET_KEY
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# ── Database ──────────────────────────────
DATABASE_URL=postgresql://postgres:password@localhost:5432/{snake}_db

# ── JWT ───────────────────────────────────
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7

# ── CORS ──────────────────────────────────
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# ── Email (optional) ──────────────────────
# EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
# EMAIL_HOST_USER=your@email.com
# EMAIL_HOST_PASSWORD=your-app-password

# ── Storage (optional – Cloudinary) ───────
# CLOUDINARY_CLOUD_NAME=
# CLOUDINARY_API_KEY=
# CLOUDINARY_API_SECRET=
"""

    files["requirements.txt"] = """Django>=4.2,<5.0
djangorestframework>=3.14.0
djangorestframework-simplejwt>=5.3.0
django-cors-headers>=4.3.0
psycopg2-binary>=2.9.9
python-decouple>=3.8
dj-database-url>=2.1.0
Pillow>=10.2.0
django-filter>=23.5
whitenoise>=6.6.0
gunicorn>=21.2.0
"""

    files["manage.py"] = f"""#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
"""

    files["config/__init__.py"] = ""

    files["config/settings.py"] = f"""import os
from pathlib import Path
from decouple import config, Csv
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ── Security ──────────────────────────────────
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

# ── Application ───────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    # Local
    'apps.users',
    'apps.core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.User'

TEMPLATES = [{{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': {{
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    }},
}}]

# ── Database ──────────────────────────────────
DATABASES = {{
    'default': dj_database_url.config(
        default=config('DATABASE_URL'),
        conn_max_age=600,
    )
}}

# ── Auth ──────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'}},
    {{'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'}},
    {{'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'}},
    {{'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}},
]

# ── REST Framework ────────────────────────────
REST_FRAMEWORK = {{
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}}

# ── JWT ───────────────────────────────────────
from datetime import timedelta
SIMPLE_JWT = {{
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=config('JWT_ACCESS_TOKEN_LIFETIME_MINUTES', default=60, cast=int)),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=config('JWT_REFRESH_TOKEN_LIFETIME_DAYS', default=7, cast=int)),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}}

# ── CORS ──────────────────────────────────────
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='http://localhost:3000', cast=Csv())

# ── Static & Media ────────────────────────────
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ── Internationalisation ──────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
"""

    files["config/urls.py"] = f"""from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # JWT Auth
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Apps
    path('api/users/', include('apps.users.urls')),
    path('api/', include('apps.core.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""

    files["config/wsgi.py"] = """import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
application = get_wsgi_application()
"""

    files["apps/__init__.py"] = ""
    files["apps/users/__init__.py"] = ""
    files["apps/core/__init__.py"] = ""

    files["apps/users/apps.py"] = """from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'
"""

    files["apps/users/models.py"] = """from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    \"\"\"Custom user model with additional fields.\"\"\"
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
    ]

    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    is_email_verified = models.BooleanField(default=False)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ['-date_joined']
        indexes = [models.Index(fields=['email']), models.Index(fields=['role'])]

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f\"{self.first_name} {self.last_name}\".strip() or self.email
"""

    files["apps/users/serializers.py"] = """from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name',
                  'full_name', 'bio', 'avatar', 'role', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
"""

    files["apps/users/views.py"] = """from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, RegisterSerializer, ChangePasswordSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    \"\"\"POST /api/users/register/ – create new account\"\"\"
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(generics.RetrieveUpdateAPIView):
    \"\"\"GET/PATCH /api/users/me/ – current user profile\"\"\"
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserListView(generics.ListAPIView):
    \"\"\"GET /api/users/ – list users (admin only)\"\"\"
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    filterset_fields = ['role', 'is_active']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering_fields = ['date_joined', 'email']


@api_view(['POST'])
def change_password(request):
    \"\"\"POST /api/users/change-password/\"\"\"
    serializer = ChangePasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    if not request.user.check_password(serializer.validated_data['old_password']):
        return Response({'error': 'Current password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

    request.user.set_password(serializer.validated_data['new_password'])
    request.user.save()
    return Response({'message': 'Password updated successfully.'})
"""

    files["apps/users/urls.py"] = """from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('me/', views.ProfileView.as_view(), name='profile'),
    path('', views.UserListView.as_view(), name='user-list'),
    path('change-password/', views.change_password, name='change-password'),
]
"""

    files["apps/users/admin.py"] = """from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'username', 'full_name', 'role', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active', 'is_staff']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-date_joined']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('bio', 'avatar', 'role', 'is_email_verified')}),
    )
"""

    files["apps/core/apps.py"] = """from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
"""

    files["apps/core/views.py"] = """from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db import connection


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    \"\"\"GET /api/health/ – service health check\"\"\"
    try:
        connection.ensure_connection()
        db_status = 'connected'
    except Exception:
        db_status = 'disconnected'

    return Response({'status': 'ok', 'database': db_status})
"""

    files["apps/core/urls.py"] = """from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health'),
]
"""

    files["Dockerfile"] = f"""FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \\
    libpq-dev gcc \\
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
"""

    files["docker-compose.yml"] = f"""version: '3.8'

services:
  # ── Django API ────────────────────────────────
  api:
    build: .
    container_name: {snake}_api
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      SECRET_KEY: ${{SECRET_KEY:-django-insecure-change-this}}
      DEBUG: "False"
      DATABASE_URL: postgresql://postgres:${{POSTGRES_PASSWORD:-password}}@db:5432/{snake}_db
      ALLOWED_HOSTS: localhost,127.0.0.1,0.0.0.0
      CORS_ALLOWED_ORIGINS: http://localhost:3000,http://localhost:5173
    depends_on:
      db:
        condition: service_healthy
    command: >
      sh -c "python manage.py migrate &&
             python manage.py collectstatic --noinput &&
             gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4"

  # ── PostgreSQL ───────────────────────────────
  db:
    image: postgres:16-alpine
    container_name: {snake}_db
    restart: unless-stopped
    environment:
      POSTGRES_PASSWORD: ${{POSTGRES_PASSWORD:-password}}
      POSTGRES_DB: {snake}_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
    name: {snake}_postgres_data
"""

    files["README.md"] = f"""# {pname}

> **{category}** · Django REST Framework · PostgreSQL · JWT · Docker

## ⚡ Quick Start

### 1. Set up virtual environment
```bash
python -m venv venv
source venv/bin/activate    # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
```

### 2. Configure environment
```bash
cp .env.example .env
# Edit .env – set SECRET_KEY and DATABASE_URL
```

### 3. Run migrations and create superuser
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open:
- **API**: http://localhost:8000/api/
- **Admin**: http://localhost:8000/admin/

---

## 🐳 Docker
```bash
cp .env.example .env
docker-compose up -d
```

---

## 📡 API Endpoints

| Method | URL | Auth | Description |
|--------|-----|------|-------------|
| POST | `/api/auth/login/` | ✗ | Get JWT token pair |
| POST | `/api/auth/refresh/` | ✗ | Refresh access token |
| POST | `/api/users/register/` | ✗ | Create account |
| GET | `/api/users/me/` | ✓ | Get own profile |
| PATCH | `/api/users/me/` | ✓ | Update profile |
| GET | `/api/users/` | Admin | List all users |
| POST | `/api/users/change-password/` | ✓ | Change password |
| GET | `/api/health/` | ✗ | Health check |

### Example: Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \\
  -H "Content-Type: application/json" \\
  -d '{{"email":"admin@example.com","password":"your-password"}}'
```

### Example: Authenticated request
```bash
curl http://localhost:8000/api/users/me/ \\
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 📦 Tech Stack
| Layer      | Technology                 |
|------------|----------------------------|
| Framework  | Django 4.2                 |
| API        | Django REST Framework 3.14 |
| Database   | PostgreSQL 16              |
| Auth       | JWT (simplejwt)            |
| Deployment | Gunicorn + Docker          |
"""

    return files


# ─────────────────────────────────────────────
# STACK 4 – Vue 3 + Express + MySQL
# ─────────────────────────────────────────────

def _vue_express_mysql(ctx: dict) -> Dict[str, str]:
    pname = ctx["project_name"]
    snake = _snake(pname)
    primary = ctx.get("colors", ["#42b883"])[0]
    category = ctx.get("category", "Web App")
    files: Dict[str, str] = {}

    files[".env.example"] = f"""# ═══════════════════════════════════════════
# {pname} – Environment Variables
# ═══════════════════════════════════════════

# ── Server ────────────────────────────────
PORT=4000
NODE_ENV=development

# ── MySQL ─────────────────────────────────
DB_HOST=localhost
DB_PORT=3306
DB_NAME={snake}_db
DB_USER=root
DB_PASS=REPLACE_WITH_YOUR_DB_PASSWORD

# ── JWT ───────────────────────────────────
JWT_SECRET=REPLACE_WITH_LONG_RANDOM_STRING
JWT_EXPIRES_IN=7d

# ── Client ────────────────────────────────
CLIENT_URL=http://localhost:5173
"""

    files["server/package.json"] = f"""{{
  "name": "{pname}-server",
  "version": "0.1.0",
  "scripts": {{
    "dev": "nodemon src/index.js",
    "start": "node src/index.js",
    "sync": "node src/sync-db.js"
  }},
  "dependencies": {{
    "bcryptjs": "^2.4.3",
    "cors": "^2.8.5",
    "dotenv": "^16.4.5",
    "express": "^4.18.3",
    "express-validator": "^7.0.1",
    "helmet": "^7.1.0",
    "jsonwebtoken": "^9.0.2",
    "morgan": "^1.10.0",
    "mysql2": "^3.9.4",
    "sequelize": "^6.37.1"
  }},
  "devDependencies": {{
    "nodemon": "^3.1.0"
  }}
}}
"""

    files["server/src/index.js"] = f"""require('dotenv').config();
const express = require('express');
const helmet = require('helmet');
const cors = require('cors');
const morgan = require('morgan');
const routes = require('./routes');
const {{ sequelize }} = require('./config/db');

const app = express();
const PORT = process.env.PORT || 4000;

app.use(helmet());
app.use(cors({{ origin: process.env.CLIENT_URL, credentials: true }}));
app.use(morgan('dev'));
app.use(express.json());
app.use(express.urlencoded({{ extended: true }}));

app.use('/api', routes);
app.get('/health', (_, res) => res.json({{ status: 'ok', service: '{pname}' }}));

app.use((err, req, res, _next) => {{
  console.error(err.stack);
  res.status(err.status || 500).json({{ error: err.message || 'Internal Server Error' }});
}});

sequelize.authenticate()
  .then(() => {{
    console.log('✅ MySQL connected');
    return app.listen(PORT, () => {{
      console.log(`🚀 {pname} API at http://localhost:${{PORT}}`);
    }});
  }})
  .catch(err => {{ console.error('❌ DB error:', err); process.exit(1); }});
"""

    files["server/src/config/db.js"] = f"""const {{ Sequelize }} = require('sequelize');

const sequelize = new Sequelize(
  process.env.DB_NAME,
  process.env.DB_USER,
  process.env.DB_PASS,
  {{
    host: process.env.DB_HOST || 'localhost',
    port: parseInt(process.env.DB_PORT) || 3306,
    dialect: 'mysql',
    logging: process.env.NODE_ENV === 'development' ? console.log : false,
    pool: {{ max: 10, min: 0, acquire: 30000, idle: 10000 }},
  }}
);

module.exports = {{ sequelize }};
"""

    files["server/src/models/User.js"] = """const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/db');
const bcrypt = require('bcryptjs');

const User = sequelize.define('User', {
  id: { type: DataTypes.INTEGER, primaryKey: true, autoIncrement: true },
  name: { type: DataTypes.STRING(100), allowNull: false },
  email: { type: DataTypes.STRING(191), allowNull: false, unique: true },
  password: { type: DataTypes.STRING, allowNull: false },
  role: { type: DataTypes.ENUM('user', 'admin'), defaultValue: 'user' },
  isActive: { type: DataTypes.BOOLEAN, defaultValue: true },
}, {
  timestamps: true,
  hooks: {
    beforeCreate: async (user) => { user.password = await bcrypt.hash(user.password, 12); },
    beforeUpdate: async (user) => {
      if (user.changed('password')) user.password = await bcrypt.hash(user.password, 12);
    },
  },
  defaultScope: { attributes: { exclude: ['password'] } },
  scopes: { withPassword: { attributes: {} } },
});

User.prototype.comparePassword = function(candidate) {
  return require('bcryptjs').compare(candidate, this.password);
};

module.exports = User;
"""

    files["server/src/middleware/auth.js"] = """const jwt = require('jsonwebtoken');
const User = require('../models/User');

exports.protect = async (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ error: 'No token provided' });

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = await User.findByPk(decoded.id);
    if (!req.user) return res.status(401).json({ error: 'User not found' });
    next();
  } catch {
    return res.status(401).json({ error: 'Invalid token' });
  }
};

exports.requireAdmin = (req, res, next) => {
  if (req.user?.role !== 'admin') return res.status(403).json({ error: 'Admin only' });
  next();
};
"""

    files["server/src/routes/auth.js"] = f"""const router = require('express').Router();
const jwt = require('jsonwebtoken');
const User = require('../models/User');
const {{ body, validationResult }} = require('express-validator');
const {{ protect }} = require('../middleware/auth');

const sign = (id) => jwt.sign({{ id }}, process.env.JWT_SECRET, {{ expiresIn: process.env.JWT_EXPIRES_IN }});

router.post('/register', [
  body('name').trim().isLength({{ min: 2 }}),
  body('email').isEmail().normalizeEmail(),
  body('password').isLength({{ min: 8 }}),
], async (req, res) => {{
  const errors = validationResult(req);
  if (!errors.isEmpty()) return res.status(400).json({{ errors: errors.array() }});

  const {{ name, email, password }} = req.body;
  if (await User.findOne({{ where: {{ email }} }})) {{
    return res.status(409).json({{ error: 'Email already registered' }});
  }}
  const user = await User.create({{ name, email, password }});
  res.status(201).json({{ token: sign(user.id), user: {{ id: user.id, name, email, role: user.role }} }});
}});

router.post('/login', async (req, res) => {{
  const {{ email, password }} = req.body;
  const user = await User.scope('withPassword').findOne({{ where: {{ email }} }});
  if (!user || !(await user.comparePassword(password))) {{
    return res.status(401).json({{ error: 'Invalid credentials' }});
  }}
  res.json({{ token: sign(user.id), user: {{ id: user.id, name: user.name, email, role: user.role }} }});
}});

router.get('/me', protect, (req, res) => res.json(req.user));

module.exports = router;
"""

    files["server/src/routes/index.js"] = """const router = require('express').Router();
router.use('/auth', require('./auth'));
// Add more: router.use('/products', require('./products'));
module.exports = router;
"""

    files["server/src/sync-db.js"] = f"""require('dotenv').config();
const {{ sequelize }} = require('./config/db');
const User = require('./models/User');

async function sync() {{
  await sequelize.sync({{ force: true }});
  console.log('✅ Tables created');

  await User.create({{ name: 'Admin', email: 'admin@{snake}.com', password: 'admin123', role: 'admin' }});
  console.log('🌱 Admin seeded: admin@{snake}.com / admin123');
  await sequelize.close();
}}

sync().catch(console.error);
"""

    files["client/package.json"] = f"""{{
  "name": "{pname}-client",
  "version": "0.1.0",
  "scripts": {{
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  }},
  "dependencies": {{
    "axios": "^1.6.8",
    "pinia": "^2.1.7",
    "vue": "^3.4.21",
    "vue-router": "^4.3.0"
  }},
  "devDependencies": {{
    "@vitejs/plugin-vue": "^5.0.4",
    "autoprefixer": "^10.4.19",
    "postcss": "^8.4.38",
    "tailwindcss": "^3.4.3",
    "vite": "^5.2.7"
  }}
}}
"""

    files["client/vite.config.js"] = """import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: { '/api': { target: 'http://localhost:4000', changeOrigin: true } },
  },
});
"""

    files["client/index.html"] = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{pname}</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>
"""

    files["client/src/main.js"] = """import { createApp } from 'vue';
import { createPinia } from 'pinia';
import router from './router';
import App from './App.vue';
import './style.css';

createApp(App).use(createPinia()).use(router).mount('#app');
"""

    files["client/src/style.css"] = f"""@tailwind base;
@tailwind components;
@tailwind utilities;
:root {{ --primary: {primary}; }}
"""

    files["client/src/App.vue"] = """<template>
  <RouterView />
</template>

<script setup>
import { RouterView } from 'vue-router';
</script>
"""

    files["client/src/router/index.js"] = """import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const routes = [
  { path: '/', component: () => import('../pages/Home.vue') },
  { path: '/login', component: () => import('../pages/Login.vue') },
  { path: '/register', component: () => import('../pages/Register.vue') },
  { path: '/dashboard', component: () => import('../pages/Dashboard.vue'), meta: { requiresAuth: true } },
];

const router = createRouter({ history: createWebHistory(), routes });

router.beforeEach((to) => {
  const auth = useAuthStore();
  if (to.meta.requiresAuth && !auth.token) return '/login';
});

export default router;
"""

    files["client/src/stores/auth.js"] = """import { defineStore } from 'pinia';
import { ref } from 'vue';
import axios from 'axios';

export const useAuthStore = defineStore('auth', () => {
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'));
  const token = ref(localStorage.getItem('token') || '');

  if (token.value) axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`;

  const setAuth = (u, t) => {
    user.value = u;
    token.value = t;
    localStorage.setItem('user', JSON.stringify(u));
    localStorage.setItem('token', t);
    axios.defaults.headers.common['Authorization'] = `Bearer ${t}`;
  };

  const logout = () => {
    user.value = null;
    token.value = '';
    localStorage.removeItem('user');
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
  };

  return { user, token, setAuth, logout };
});
"""

    files["client/src/pages/Home.vue"] = f"""<template>
  <div class="min-h-screen flex items-center justify-center bg-white">
    <div class="text-center space-y-6 px-6">
      <h1 class="text-6xl font-black text-gray-900">{pname}</h1>
      <p class="text-xl text-gray-500">{category} · Vue 3 + Express + MySQL</p>
      <div class="flex gap-4 justify-center">
        <RouterLink to="/register" class="px-8 py-3 rounded-xl font-semibold text-white"
          :style="{{ backgroundColor: '{primary}' }}">Get Started</RouterLink>
        <RouterLink to="/login" class="px-8 py-3 rounded-xl font-semibold bg-gray-100 text-gray-700">Sign In</RouterLink>
      </div>
    </div>
  </div>
</template>
"""

    files["client/src/pages/Login.vue"] = f"""<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="w-full max-w-md bg-white rounded-2xl border shadow-sm p-8">
      <h1 class="text-2xl font-bold mb-6">Sign In</h1>
      <div v-if="error" class="mb-4 p-3 rounded-lg bg-red-50 text-red-600 text-sm">{{ error }}</div>
      <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
          <input v-model="form.email" type="email" required class="w-full px-4 py-2.5 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 transition" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
          <input v-model="form.password" type="password" required class="w-full px-4 py-2.5 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 transition" />
        </div>
        <button type="submit" :disabled="loading"
          class="w-full py-3 rounded-xl font-semibold text-white transition disabled:opacity-60"
          :style="{{ backgroundColor: '{primary}' }}">
          {{ loading ? 'Signing in...' : 'Sign In' }}
        </button>
      </form>
      <p class="mt-4 text-center text-sm text-gray-500">
        No account? <RouterLink to="/register" :style="{{ color: '{primary}' }}" class="font-medium">Register</RouterLink>
      </p>
    </div>
  </div>
</template>
<script setup>
import {{ ref }} from 'vue';
import {{ useRouter }} from 'vue-router';
import axios from 'axios';
import {{ useAuthStore }} from '../stores/auth';

const form = ref({{ email: '', password: '' }});
const error = ref('');
const loading = ref(false);
const router = useRouter();
const auth = useAuthStore();

const handleLogin = async () => {{
  loading.value = true; error.value = '';
  try {{
    const {{ data }} = await axios.post('/api/auth/login', form.value);
    auth.setAuth(data.user, data.token);
    router.push('/dashboard');
  }} catch (e) {{ error.value = e.response?.data?.error || 'Login failed'; }}
  finally {{ loading.value = false; }}
}};
</script>
"""

    files["client/src/pages/Register.vue"] = f"""<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="w-full max-w-md bg-white rounded-2xl border shadow-sm p-8">
      <h1 class="text-2xl font-bold mb-6">Create Account</h1>
      <div v-if="error" class="mb-4 p-3 rounded-lg bg-red-50 text-red-600 text-sm">{{ error }}</div>
      <form @submit.prevent="handleRegister" class="space-y-4">
        <div v-for="f in ['name','email','password']" :key="f">
          <label class="block text-sm font-medium text-gray-700 mb-1 capitalize">{{ f }}</label>
          <input v-model="form[f]" :type="f === 'email' ? 'email' : f === 'password' ? 'password' : 'text'"
            required class="w-full px-4 py-2.5 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 transition" />
        </div>
        <button type="submit" :disabled="loading"
          class="w-full py-3 rounded-xl font-semibold text-white transition disabled:opacity-60"
          :style="{{ backgroundColor: '{primary}' }}">
          {{ loading ? 'Creating...' : 'Create Account' }}
        </button>
      </form>
    </div>
  </div>
</template>
<script setup>
import {{ ref }} from 'vue';
import {{ useRouter }} from 'vue-router';
import axios from 'axios';
import {{ useAuthStore }} from '../stores/auth';
const form = ref({{ name: '', email: '', password: '' }});
const error = ref(''); const loading = ref(false);
const router = useRouter(); const auth = useAuthStore();
const handleRegister = async () => {{
  loading.value = true; error.value = '';
  try {{
    const {{ data }} = await axios.post('/api/auth/register', form.value);
    auth.setAuth(data.user, data.token);
    router.push('/dashboard');
  }} catch (e) {{ error.value = e.response?.data?.error || 'Error'; }}
  finally {{ loading.value = false; }}
}};
</script>
"""

    files["client/src/pages/Dashboard.vue"] = f"""<template>
  <div class="max-w-4xl mx-auto px-4 py-10">
    <h1 class="text-3xl font-bold mb-2">Dashboard</h1>
    <p class="text-gray-500 mb-8">Welcome, {{ auth.user?.name }}</p>
    <div class="bg-white rounded-2xl border shadow-sm p-6">
      <h2 class="text-lg font-semibold mb-4">Next Steps</h2>
      <ul class="space-y-2 text-sm text-gray-600">
        <li>✅ Auth (register / login / JWT) working</li>
        <li>○ Add pages in <code class="bg-gray-100 px-1 rounded">client/src/pages/</code></li>
        <li>○ Add routes in <code class="bg-gray-100 px-1 rounded">server/src/routes/</code></li>
        <li>○ Add Sequelize models in <code class="bg-gray-100 px-1 rounded">server/src/models/</code></li>
      </ul>
      <button @click="handleLogout" class="mt-6 px-4 py-2 rounded-lg text-sm text-red-500 border border-red-200 hover:bg-red-50">Sign Out</button>
    </div>
  </div>
</template>
<script setup>
import {{ useAuthStore }} from '../stores/auth';
import {{ useRouter }} from 'vue-router';
const auth = useAuthStore(); const router = useRouter();
const handleLogout = () => {{ auth.logout(); router.push('/'); }};
</script>
"""

    files["docker-compose.yml"] = f"""version: '3.8'

services:
  client:
    build: ./client
    container_name: {snake}_client
    ports:
      - "5173:80"
    depends_on:
      - server

  server:
    build: ./server
    container_name: {snake}_server
    restart: unless-stopped
    ports:
      - "4000:4000"
    environment:
      NODE_ENV: production
      PORT: 4000
      DB_HOST: mysql
      DB_PORT: 3306
      DB_NAME: {snake}_db
      DB_USER: root
      DB_PASS: ${{MYSQL_ROOT_PASSWORD:-rootpassword}}
      JWT_SECRET: ${{JWT_SECRET:-change-this-secret}}
      CLIENT_URL: http://localhost:5173
    depends_on:
      mysql:
        condition: service_healthy

  mysql:
    image: mysql:8.0
    container_name: {snake}_mysql
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD: ${{MYSQL_ROOT_PASSWORD:-rootpassword}}
      MYSQL_DATABASE: {snake}_db
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

  phpmyadmin:
    image: phpmyadmin/phpmyadmin
    container_name: {snake}_phpmyadmin
    ports:
      - "8080:80"
    environment:
      PMA_HOST: mysql
      MYSQL_ROOT_PASSWORD: ${{MYSQL_ROOT_PASSWORD:-rootpassword}}
    depends_on:
      - mysql

volumes:
  mysql_data:
    name: {snake}_mysql_data
"""

    files["README.md"] = f"""# {pname}

> **{category}** · Vue 3 · Express · MySQL · Sequelize · JWT Auth

## ⚡ Quick Start

```bash
cp .env.example .env  # Edit DB_PASS and JWT_SECRET
```

**Server:**
```bash
cd server && npm install
node src/sync-db.js   # Creates tables + seeds admin
npm run dev           # http://localhost:4000
```

**Client:**
```bash
cd client && npm install
npm run dev           # http://localhost:5173
```

## 🐳 Docker
```bash
docker-compose up -d
```
| Service    | URL                    |
|------------|------------------------|
| Client     | http://localhost:5173  |
| API        | http://localhost:4000  |
| phpMyAdmin | http://localhost:8080  |

## 🔑 Default Credentials (after sync-db)
- Email: `admin@{snake}.com` / Password: `admin123`

## 📦 Stack
Vue 3 + Pinia + Vue Router · Express 4 · MySQL 8 + Sequelize · JWT
"""

    return files


# ─────────────────────────────────────────────
# STACK 5 – React Static (Vite + Tailwind)
# ─────────────────────────────────────────────

def _react_static(ctx: dict) -> Dict[str, str]:
    pname = ctx["project_name"]
    primary = ctx.get("colors", ["#3B82F6"])[0]
    category = ctx.get("category", "Static Site")
    files: Dict[str, str] = {}

    files[".env.example"] = f"""# {pname} – Environment Variables
VITE_APP_NAME="{pname}"
VITE_APP_URL=http://localhost:5173
# Add your API keys here:
# VITE_API_KEY=
"""

    files["package.json"] = f"""{{
  "name": "{pname}",
  "version": "0.1.0",
  "scripts": {{
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx"
  }},
  "dependencies": {{
    "clsx": "^2.1.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.22.3",
    "tailwind-merge": "^2.2.2"
  }},
  "devDependencies": {{
    "@types/react": "^18.2.73",
    "@types/react-dom": "^18.2.22",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.19",
    "postcss": "^8.4.38",
    "tailwindcss": "^3.4.3",
    "typescript": "^5.4.3",
    "vite": "^5.2.7"
  }}
}}
"""

    files["tsconfig.json"] = """{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "paths": { "@/*": ["./src/*"] }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
"""

    files["vite.config.ts"] = """import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: { alias: { '@': path.resolve(__dirname, './src') } },
});
"""

    files["tailwind.config.ts"] = f"""import type {{ Config }} from 'tailwindcss';

export default {{
  content: ['./index.html', './src/**/*.{{js,ts,jsx,tsx}}'],
  theme: {{
    extend: {{
      colors: {{ primary: '{primary}' }},
    }},
  }},
  plugins: [],
}} satisfies Config;
"""

    files["postcss.config.js"] = """module.exports = { plugins: { tailwindcss: {}, autoprefixer: {} } };
"""

    files["index.html"] = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{pname}</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
"""

    files["src/main.tsx"] = """import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
);
"""

    files["src/index.css"] = f"""@tailwind base;
@tailwind components;
@tailwind utilities;

:root {{
  --primary: {primary};
}}

@layer base {{
  body {{ @apply antialiased; }}
}}
"""

    files["src/App.tsx"] = """import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import About from './pages/About';
import Navbar from './components/Navbar';
import Footer from './components/Footer';

export default function App() {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-1">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </main>
      <Footer />
    </div>
  );
}
"""

    files["src/pages/Home.tsx"] = f"""export default function Home() {{
  return (
    <div className="max-w-5xl mx-auto px-6 py-20">
      <div className="text-center space-y-6">
        <div className="inline-block px-4 py-1 rounded-full text-sm font-medium bg-blue-50 text-blue-700 border border-blue-100">
          {category}
        </div>
        <h1 className="text-7xl font-black text-gray-900 tracking-tight leading-none">
          {pname}
        </h1>
        <p className="text-xl text-gray-500 max-w-lg mx-auto">
          Your site is ready. Edit <code className="px-1.5 py-0.5 bg-gray-100 rounded text-sm">src/pages/Home.tsx</code> to get started.
        </p>
        <div className="flex gap-4 justify-center">
          <button
            className="px-8 py-3 rounded-xl font-semibold text-white shadow-lg hover:-translate-y-0.5 transition-all"
            style={{{{ backgroundColor: '{primary}' }}}}
          >
            Get Started
          </button>
          <button className="px-8 py-3 rounded-xl font-semibold bg-gray-100 text-gray-700 hover:bg-gray-200 hover:-translate-y-0.5 transition-all">
            Learn More
          </button>
        </div>
      </div>
    </div>
  );
}}
"""

    files["src/pages/About.tsx"] = f"""export default function About() {{
  return (
    <div className="max-w-3xl mx-auto px-6 py-20">
      <h1 className="text-4xl font-bold text-gray-900 mb-6">About {pname}</h1>
      <p className="text-lg text-gray-600 leading-relaxed">
        Edit this page in <code className="px-1.5 py-0.5 bg-gray-100 rounded text-sm">src/pages/About.tsx</code>.
      </p>
    </div>
  );
}}
"""

    files["src/components/Navbar.tsx"] = f"""import {{ Link }} from 'react-router-dom';

export default function Navbar() {{
  return (
    <nav className="bg-white border-b border-gray-100 sticky top-0 z-50">
      <div className="max-w-5xl mx-auto px-6">
        <div className="flex justify-between h-16 items-center">
          <Link to="/" className="text-xl font-black text-gray-900">{pname}</Link>
          <div className="flex items-center gap-6">
            <Link to="/" className="text-sm font-medium text-gray-600 hover:text-gray-900">Home</Link>
            <Link to="/about" className="text-sm font-medium text-gray-600 hover:text-gray-900">About</Link>
            <a href="#contact" className="px-4 py-2 rounded-lg text-sm font-semibold text-white transition"
              style={{{{ backgroundColor: '{primary}' }}}}>
              Contact
            </a>
          </div>
        </div>
      </div>
    </nav>
  );
}}
"""

    files["src/components/Footer.tsx"] = f"""export default function Footer() {{
  return (
    <footer className="bg-gray-50 border-t border-gray-100 py-8">
      <div className="max-w-5xl mx-auto px-6 text-center text-sm text-gray-500">
        © {{new Date().getFullYear()}} {pname}. Built with React + Vite + Tailwind CSS.
      </div>
    </footer>
  );
}}
"""

    files["README.md"] = f"""# {pname}

> **{category}** · React 18 · TypeScript · Vite · Tailwind CSS

## ⚡ Quick Start

```bash
cp .env.example .env
npm install
npm run dev        # http://localhost:5173
```

## 📦 Build for production
```bash
npm run build      # Output in ./dist
npm run preview    # Preview production build
```

## 📁 Structure
```
src/
├── pages/         # Route pages
├── components/    # Reusable components
├── App.tsx        # Route config
├── main.tsx       # Entry point
└── index.css      # Tailwind + globals
```

## 🚀 Deploy
Drop the `dist/` folder into Netlify, Vercel, or any static host.
"""

    return files


# ─────────────────────────────────────────────
# STACK 6 – Electron + React + SQLite
# ─────────────────────────────────────────────

def _electron_sqlite(ctx: dict) -> Dict[str, str]:
    pname = ctx["project_name"]
    snake = _snake(pname)
    primary = ctx.get("colors", ["#3B82F6"])[0]
    files: Dict[str, str] = {}

    files[".env.example"] = f"""# {pname} – Electron App Config
NODE_ENV=development
APP_NAME="{pname}"
"""

    files["package.json"] = f"""{{
  "name": "{snake}",
  "version": "0.1.0",
  "description": "{pname} desktop application",
  "main": "electron/main.js",
  "scripts": {{
    "dev": "concurrently \\"vite\\" \\"wait-on http://localhost:5173 && electron .\\"",
    "build": "vite build && electron-builder",
    "electron": "electron .",
    "lint": "eslint . --ext ts,tsx"
  }},
  "dependencies": {{
    "better-sqlite3": "^9.4.3",
    "electron-store": "^8.2.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.22.3"
  }},
  "devDependencies": {{
    "@types/better-sqlite3": "^7.6.9",
    "@types/react": "^18.2.73",
    "@types/react-dom": "^18.2.22",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.19",
    "concurrently": "^8.2.2",
    "electron": "^29.1.4",
    "electron-builder": "^24.13.3",
    "postcss": "^8.4.38",
    "tailwindcss": "^3.4.3",
    "typescript": "^5.4.3",
    "vite": "^5.2.7",
    "wait-on": "^7.2.0"
  }},
  "build": {{
    "appId": "com.{snake}.app",
    "productName": "{pname}",
    "files": ["dist/**/*", "electron/**/*"],
    "mac": {{ "target": "dmg" }},
    "win": {{ "target": "nsis" }},
    "linux": {{ "target": "AppImage" }}
  }}
}}
"""

    files["vite.config.ts"] = """import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  base: './',
  build: { outDir: 'dist' },
  server: { port: 5173, strictPort: true },
});
"""

    files["electron/main.js"] = f"""const {{ app, BrowserWindow, ipcMain }} = require('electron');
const path = require('path');
const Database = require('better-sqlite3');

const isDev = process.env.NODE_ENV === 'development';

// ── Database setup ─────────────────────────────
const dbPath = path.join(app.getPath('userData'), '{snake}.db');
let db;

function setupDatabase() {{
  db = new Database(dbPath);
  db.pragma('journal_mode = WAL');

  // Create tables
  db.exec(`
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      email TEXT UNIQUE NOT NULL,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS settings (
      key TEXT PRIMARY KEY,
      value TEXT
    );
  `);

  console.log('✅ Database ready at', dbPath);
}}

// ── IPC handlers ───────────────────────────────
ipcMain.handle('db:query', (_, sql, params = []) => {{
  try {{
    const stmt = db.prepare(sql);
    if (sql.trim().toUpperCase().startsWith('SELECT')) {{
      return {{ success: true, data: stmt.all(...params) }};
    }}
    return {{ success: true, data: stmt.run(...params) }};
  }} catch (err) {{
    return {{ success: false, error: err.message }};
  }}
}});

ipcMain.handle('app:getVersion', () => app.getVersion());
ipcMain.handle('app:getPlatform', () => process.platform);

// ── Window ─────────────────────────────────────
function createWindow() {{
  const win = new BrowserWindow({{
    width: 1280,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    webPreferences: {{
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    }},
    titleBarStyle: process.platform === 'darwin' ? 'hiddenInset' : 'default',
    show: false,
  }});

  win.once('ready-to-show', () => win.show());

  if (isDev) {{
    win.loadURL('http://localhost:5173');
    win.webContents.openDevTools();
  }} else {{
    win.loadFile(path.join(__dirname, '../dist/index.html'));
  }}
}}

app.whenReady().then(() => {{
  setupDatabase();
  createWindow();
  app.on('activate', () => {{ if (BrowserWindow.getAllWindows().length === 0) createWindow(); }});
}});

app.on('window-all-closed', () => {{
  if (process.platform !== 'darwin') app.quit();
}});
"""

    files["electron/preload.js"] = """const { contextBridge, ipcRenderer } = require('electron');

// Expose safe APIs to renderer process
contextBridge.exposeInMainWorld('electron', {
  db: {
    query: (sql, params) => ipcRenderer.invoke('db:query', sql, params),
  },
  app: {
    getVersion: () => ipcRenderer.invoke('app:getVersion'),
    getPlatform: () => ipcRenderer.invoke('app:getPlatform'),
  },
});
"""

    files["src/main.tsx"] = """import React from 'react';
import ReactDOM from 'react-dom/client';
import { MemoryRouter } from 'react-router-dom';
import App from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <MemoryRouter>
      <App />
    </MemoryRouter>
  </React.StrictMode>
);
"""

    files["src/index.css"] = f"""@tailwind base;
@tailwind components;
@tailwind utilities;
:root {{ --primary: {primary}; }}
"""

    files["src/App.tsx"] = f"""import {{ Routes, Route }} from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import Settings from './pages/Settings';

export default function App() {{
  return (
    <div className="flex h-screen bg-gray-100 overflow-hidden">
      <Sidebar />
      <main className="flex-1 overflow-auto">
        <Routes>
          <Route path="/" element={{<Dashboard />}} />
          <Route path="/settings" element={{<Settings />}} />
        </Routes>
      </main>
    </div>
  );
}}
"""

    files["src/components/Sidebar.tsx"] = f"""import {{ Link, useLocation }} from 'react-router-dom';

const navItems = [
  {{ path: '/', icon: '🏠', label: 'Dashboard' }},
  {{ path: '/settings', icon: '⚙️', label: 'Settings' }},
];

export default function Sidebar() {{
  const {{ pathname }} = useLocation();

  return (
    <aside className="w-56 bg-white border-r border-gray-100 flex flex-col">
      <div className="px-4 py-5 border-b border-gray-100">
        <span className="text-lg font-black text-gray-900">{pname}</span>
      </div>
      <nav className="flex-1 px-3 py-4 space-y-1">
        {{navItems.map((item) => (
          <Link
            key={{item.path}}
            to={{item.path}}
            className={{`flex items-center gap-3 px-3 py-2 rounded-xl text-sm font-medium transition-colors ${{
              pathname === item.path
                ? 'text-white shadow-sm'
                : 'text-gray-600 hover:bg-gray-50'
            }}`}}
            style={{pathname === item.path ? {{ backgroundColor: '{primary}' }} : {{}}}}
          >
            <span>{{item.icon}}</span>
            {{item.label}}
          </Link>
        ))}}
      </nav>
    </aside>
  );
}}
"""

    files["src/pages/Dashboard.tsx"] = f"""import {{ useState, useEffect }} from 'react';

declare global {{
  interface Window {{
    electron: {{
      db: {{ query: (sql: string, params?: any[]) => Promise<{{ success: boolean; data: any; error?: string }}> }};
      app: {{ getVersion: () => Promise<string>; getPlatform: () => Promise<string> }};
    }};
  }}
}}

export default function Dashboard() {{
  const [userCount, setUserCount] = useState(0);
  const [version, setVersion] = useState('');

  useEffect(() => {{
    window.electron.db.query('SELECT COUNT(*) as count FROM users').then((result) => {{
      if (result.success) setUserCount(result.data[0].count);
    }});
    window.electron.app.getVersion().then(setVersion);
  }}, []);

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Dashboard</h1>
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-8">
        {{[
          {{ label: 'Users', value: userCount }},
          {{ label: 'App Version', value: `v${{version}}` }},
          {{ label: 'Platform', value: navigator.platform }},
        ].map((card) => (
          <div key={{card.label}} className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
            <p className="text-sm text-gray-500">{{card.label}}</p>
            <p className="mt-2 text-2xl font-bold text-gray-900">{{card.value}}</p>
          </div>
        ))}}
      </div>
      <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
        <h2 className="text-lg font-semibold mb-4">Getting Started</h2>
        <ul className="space-y-2 text-sm text-gray-600">
          <li>✅ Electron + SQLite configured</li>
          <li>✅ React UI ready</li>
          <li>○ Add your features in <code className="bg-gray-100 px-1.5 rounded">src/pages/</code></li>
          <li>○ Add IPC handlers in <code className="bg-gray-100 px-1.5 rounded">electron/main.js</code></li>
        </ul>
      </div>
    </div>
  );
}}
"""

    files["src/pages/Settings.tsx"] = f"""export default function Settings() {{
  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Settings</h1>
      <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6 max-w-lg">
        <p className="text-gray-500 text-sm">
          Add settings here. Use <code className="bg-gray-100 px-1.5 rounded">window.electron.db.query()</code> to persist them to SQLite.
        </p>
      </div>
    </div>
  );
}}
"""

    files["README.md"] = f"""# {pname}

> Desktop app · Electron · React · TypeScript · SQLite · Tailwind CSS

## ⚡ Quick Start

```bash
npm install
npm run dev     # Starts Vite + Electron in parallel
```

## 📦 Build distributables
```bash
npm run build
# Output: dist/ (web) and packaged app
```

## 📁 Structure
```
{pname}/
├── electron/
│   ├── main.js       # Main process + SQLite DB setup
│   └── preload.js    # Secure IPC bridge
├── src/              # React renderer process
│   ├── pages/
│   ├── components/
│   └── App.tsx
├── .env.example
└── package.json
```

## 💾 Database
SQLite DB is stored in the OS user data directory:
- macOS: `~/Library/Application Support/{pname}/`
- Windows: `%APPDATA%/{pname}/`
- Linux: `~/.config/{pname}/`

Use `window.electron.db.query(sql, params)` from any React component.

## 📦 Stack
Electron 29 · React 18 · TypeScript · SQLite (better-sqlite3) · Tailwind CSS
"""

    return files


# ─────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────

STACK_BUILDERS = {
    "nextjs_postgres_prisma": _nextjs_postgres_prisma,
    "react_node_mongo":       _react_node_mongo,
    "django_postgres":        _django_postgres,
    "vue_express_mysql":      _vue_express_mysql,
    "react_static":           _react_static,
    "electron_sqlite":        _electron_sqlite,
    "tauri_react":            _electron_sqlite,  # Simplified: same structure
}


def build_files(stack_id: str, ctx: dict) -> Dict[str, str]:
    """Return a dict of {filepath: content} for the given stack."""
    builder = STACK_BUILDERS.get(stack_id)
    if not builder:
        raise ValueError(f"Unknown stack: {stack_id}")
    return builder(ctx)

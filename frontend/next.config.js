/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  // Disable telemetry
  telemetry: false,
  // Enable React strict mode for better development practices
  reactStrictMode: true,
  // Improve performance by disabling x-powered-by header
  poweredByHeader: false,
};

module.exports = nextConfig;

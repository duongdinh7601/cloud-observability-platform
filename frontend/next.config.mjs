const nextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: "http://log-service:8000/:path*",
      },
    ];
  },
};

export default nextConfig;

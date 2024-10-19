import { Link } from "wouter";

type Feature = {
  title: string;
  description: string;
  icon: string;
};

const features: Feature[] = [
  {
    title: "Detailed Analytics",
    description:
      "Get detailed analytics on your playlists, top artists, and tracks over time.",
    icon: "i-ri-bar-chart-box-line",
  },
  {
    title: "Playlist Insights",
    description:
      "Dive deep into your playlists, explore song genres, and track moods.",
    icon: "i-ri-play-list-line",
  },
  {
    title: "Personalized Stats",
    description:
      "See personalized statistics based on your listening habits and favorite artists.",
    icon: "i-ri-user-heart-line",
  },
  {
    title: "Better Search",
    description:
      "Effortlessly explore your Spotify library with advanced search capabilities." +
      "Find tracks within albums, songs in playlists, and even discover artists by " +
      "individual tracks—all in one place. ",

    icon: "i-ri-search-eye-line",
  },
];

const socials = [
  {
    icon: "i-ri-facebook-circle-line",
    hover: "i-ri-facebook-circle-fill",
    link: "#",
  },
  {
    icon: "i-ri-twitter-line",
    hover: "i-ri-twitter-fill",
    link: "#",
  },
  {
    icon: "i-ri-instagram-line",
    hover: "i-ri-instagram-fill",
    link: "#",
  },
  {
    icon: "i-ri-github-fill",
    hover: "i-ri-github-line",
    link: "#",
  },
];

export default function Home() {
  return (
    <main className="bg-green-200 text-gray-800 min-h-screen text-sm">
      <nav className="bg-white shadow-sm py-4">
        <div className="container mx-auto flex justify-between items-center px-6">
          <a href="#" className="text-emerald-500 text-2xl font-semibold">
            Dashspot
          </a>
          <div className="flex space-x-4 items-center">
            {["Features", "Docs", "Contact"].map((link) => (
              <a
                key={link}
                href="#"
                className={[
                  "text-gray-700 hover:text-emerald-500 transition-all duration-500",
                  "hover:px-4 hover:border-b-2 hover:border-emerald-500",
                ].join(" ")}
              >
                {link}
              </a>
            ))}
          </div>
        </div>
      </nav>

      <section className="container mx-auto py-20 px-6 text-center">
        <h1 className="text-4xl md:text-6xl font-bold text-gray-800 mb-4">
          Analyze Your Spotify Library
        </h1>
        <p className="text-lg md:text-xl text-gray-600 mb-8">
          Discover insights and trends in your Spotify playlists, artists, and
          more with our user-friendly dashboard.
        </p>
        <Link
          href="/signup"
          className={[
            "bg-emerald-500 text-white px-5 py-3 rounded-full",
            "font-semibold hover:bg-emerald-600 transition-all duration-500 group text-xl",
            "hover:shadow-lg hover:shadow-primary",
          ].join(" ")}
        >
          <i
            className={[
              "i-ri-spotify-line",
              "group-hover:i-ri-spotify-fill group-hover:font-bold group-hover:scale-150 mr-2 align-middle transition-all duration-500",
              "group-hover:-rotate-12",
            ].join(" ")}
          ></i>
          <span className="align-middle">Get Started</span>
        </Link>
      </section>

      <section className="bg-white py-16">
        <div className="container mx-auto px-6">
          <h2 className="text-3xl font-bold text-gray-800 text-center mb-12">
            Features
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-12">
            {features.map((feature) => (
              <div className="flex flex-col items-center text-center">
                <i
                  className={`${feature.icon} text-emerald-500 text-5xl mb-4`}
                ></i>
                <h3 className="text-xl font-semibold text-gray-800 mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="bg-emerald-500 py-20 text-white">
        <div className="container mx-auto px-6 text-center">
          <h2 className="text-4xl font-bold mb-4">
            Ready to Explore Your Spotify Data?
          </h2>
          <p className="text-lg md:text-xl mb-8">
            Get started now and gain valuable insights from your Spotify
            library!
          </p>
          <Link
            href="/signup"
            className={[
              "bg-white text-emerald-500 font-semibold",
              "px-8 py-3 rounded-full hover:shadow-lg hover:shadow-primary transition-shadow duration-500",
            ].join(" ")}
          >
            <span>Get Started with Spotify</span>
          </Link>
        </div>
      </section>

      <footer className="bg-white py-8">
        <div className="container mx-auto px-6 text-center">
          <p className="text-gray-600 mb-4">
            © 2024 Spotify Dashboard. All rights reserved.
          </p>
          <div className="flex justify-center space-x-4">
            {socials.map((social) => (
              <a
                key={social.icon}
                href={social.link}
                className={[
                  "text-2xl text-emerald-500 group group-hover:bg-gray-400",
                ].join(" ")}
              >
                <i
                  className={[
                    social.icon,
                    "transition-colors duration-500",
                    "group-hover:text-emerald-600",
                  ].join(" ")}
                ></i>
              </a>
            ))}
          </div>
        </div>
      </footer>
    </main>
  );
}

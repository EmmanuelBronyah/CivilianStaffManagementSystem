import "../styles/splashscreen.css";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

function SplashScreen() {
  const navigate = useNavigate();
  const text = "CiviBase";

  const [fadeOut, setFadeOut] = useState(false);

  useEffect(() => {
    const fadeTimer = setTimeout(() => {
      setFadeOut(true);
    }, 2800);

    const redirectTimer = setTimeout(() => {
      navigate("/auth/login");
    }, 3500);

    return () => {
      clearTimeout(fadeTimer);
      clearTimeout(redirectTimer);
    };
  }, [navigate]);

  return (
    <div className={`splash-screen ${fadeOut ? "fade-out" : ""}`}>
      <h1 className="logo-text">
        {text.split("").map((letter, index) => (
          <span
            key={index}
            className="letter"
            style={{ animationDelay: `${index * 0.2}s` }}
          >
            {letter}
          </span>
        ))}

        <span className="cursor">|</span>
      </h1>
    </div>
  );
}

export default SplashScreen;

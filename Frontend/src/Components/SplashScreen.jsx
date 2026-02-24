import style from "../styles/splashscreen.module.css";
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
    <div className={`${style.splashScreen} ${fadeOut ? style.fadeOut : ""}`}>
      <h1 className={style.logoText}>
        {text.split("").map((letter, index) => (
          <span
            key={index}
            className={style.letter}
            style={{ animationDelay: `${index * 0.2}s` }}
          >
            {letter}
          </span>
        ))}

        <span className={style.cursor}>|</span>
      </h1>
    </div>
  );
}

export default SplashScreen;

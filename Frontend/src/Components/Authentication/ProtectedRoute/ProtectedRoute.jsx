import { Navigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import api from "../../../api";
import { REFRESH_TOKEN, ACCESS_TOKEN } from "../../../constants";
import { useState, useEffect, useRef } from "react";

function ProtectedRoute({ children }) {
  const [isAuthorized, setIsAuthorized] = useState(null);
  const hasRun = useRef(false);

  useEffect(() => {
    if (hasRun.current) return;
    hasRun.current = true;

    auth().catch(() => setIsAuthorized(false));
  }, []);

  const refreshToken = async () => {
    console.log("RUN REFRESH FUNCTION");

    const refreshToken = localStorage.getItem(REFRESH_TOKEN);
    console.log("REFRESH TOKEN", refreshToken);

    try {
      const res = await api.post("/api/token-refresh/", {
        refresh: refreshToken,
      });

      if (res.status === 200) {
        localStorage.setItem(ACCESS_TOKEN, res.data.access);
        console.log("NEW ACCESS TOKEN RETRIEVED");
        setIsAuthorized(true);
      } else {
        console.log("COULD NOT RETRIEVE ACCESS TOKEN");
        setIsAuthorized(false);
      }
    } catch (error) {
      console.log("REFRESH TOKEN ERROR", error);
      localStorage.clear(ACCESS_TOKEN);
      localStorage.clear(REFRESH_TOKEN);
      setIsAuthorized(false);
    }
  };

  const auth = async () => {
    const token = localStorage.getItem(ACCESS_TOKEN);
    console.log("TOKEN IN AUTH FUNCTION", token);

    if (!token) {
      console.log("THERE IS NO TOKEN");
      setIsAuthorized(false);
      return;
    }

    const decoded = jwtDecode(token);
    console.log("DECODED TOKEN", decoded);

    const tokenExpiration = decoded.exp;
    console.log("TOKEN EXPIRATION", tokenExpiration);

    const now = Date.now() / 1000;
    console.log("NOW", now);

    if (tokenExpiration < now) {
      console.log("TOKEN HAS EXPIRED");
      await refreshToken();
    } else {
      console.log("TOKEN HAS NOT EXPIRED");
      setIsAuthorized(true);
    }
  };

  if (isAuthorized === null) {
    return <div>Loading...</div>;
  }

  return isAuthorized ? children : <Navigate to="/auth/login" />;
}

export default ProtectedRoute;

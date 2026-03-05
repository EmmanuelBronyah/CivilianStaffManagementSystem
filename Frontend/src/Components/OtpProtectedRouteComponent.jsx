import { Navigate } from "react-router-dom";
import { TEMP_TOKEN } from "../constants";

export default function ProtectOtpRoute({ children }) {
  const tempToken = localStorage.getItem(TEMP_TOKEN);

  if (!tempToken) {
    return <Navigate to="/auth/login" replace />;
  }

  return children;
}

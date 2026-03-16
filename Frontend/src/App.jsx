import { BrowserRouter, Routes, Route } from "react-router-dom";
import RegisterUser from "./Pages/RegistrationPage";
import LoginUser from "./Pages/LoginPage";
import LogoutUser from "./Pages/LogoutPage";
import ResendAndVerifyOTP from "./Pages/OTPPage";
import ResetPassword from "./Pages/ResetPasswordPage";
import ConfirmPasswordReset from "./Pages/ConfirmPasswordResetPage";
import ProtectedRoute from "./Components/ProtectedRoute";
import SplashScreen from "./Pages/SplashScreen";
import HomePage from "./Pages/HomePage";
import ProtectOtpRoute from "./Components/OtpProtectedRouteComponent";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<SplashScreen />} />
        <Route
          path="/auth/register"
          element={<RegisterUser route="api/register/" />}
        />
        <Route path="/auth/login" element={<LoginUser route="api/login/" />} />
        <Route
          path="/auth/otp"
          element={
            <ProtectOtpRoute>
              <ResendAndVerifyOTP route="api/verify-otp-token/" />
            </ProtectOtpRoute>
          }
        />
        <Route
          path="/reset-password"
          element={<ResetPassword route="api/auth/password/reset/" />}
        />
        <Route
          path="/password/reset/confirm/:uid/:token"
          element={
            <ConfirmPasswordReset route="api/auth/password/reset/confirm/" />
          }
        />
        <Route
          path="/homepage"
          element={
            <ProtectedRoute>
              <HomePage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/auth/logout"
          element={
            <ProtectedRoute>
              <LogoutUser route="api/logout/" />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;

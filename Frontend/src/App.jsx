import { BrowserRouter, Routes, Route } from "react-router-dom";
import LoginUser from "./Features/Auth/Pages/LoginPage";
import LogoutUser from "./Features/Auth/Pages/LogoutPage";
import ResendAndVerifyOTP from "./Features/Auth/Pages/OTPPage";
import ResetPassword from "./Features/Auth/Pages/ResetPasswordPage";
import ConfirmPasswordReset from "./Features/Auth/Pages/ConfirmPasswordResetPage";
import ProtectedRoute from "./Features/Auth/Components/ProtectedRoute";
import SplashScreen from "./Components/Common/SplashScreen";
import HomePage from "./Features/Homepage/Pages/HomePage";
import ProtectOtpRoute from "./Features/Auth/Components/OtpProtectedRouteComponent";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<SplashScreen />} />
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

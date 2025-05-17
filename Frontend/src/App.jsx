import { BrowserRouter, Routes, Route } from "react-router-dom";
import RegisterUser from "./Components/Authentication/Registration/UserRegistration";
import LoginUser from "./Components/Authentication/Login/UserLogin";
import LogoutUser from "./Components/Logout/UserLogout";
import ResendAndVerifyOTP from "./Components/Authentication/OTP/HandleOTP";
import ResetPassword from "./Components/Authentication/Password/ResetPassword";
import ConfirmPasswordReset from "./Components/Authentication/Password/ConfirmPasswordReset";
import ProtectedRoute from "./Components/Authentication/ProtectedRoute/ProtectedRoute";
import SplashScreen from "./Components/SplashScreen";
import Dashboard from "./Components/Dashboard";

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
          element={<ResendAndVerifyOTP route="api/verify-otp-token/" />}
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
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
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

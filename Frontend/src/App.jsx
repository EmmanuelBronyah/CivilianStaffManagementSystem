import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import LoginUser from "./Components/AuthenticationComponents/UserLogin";
import RegisterUser from "./Components/AuthenticationComponents/UserRegistration";
import ResendAndVerifyOTP from "./Components/AuthenticationComponents/HandleOTP";
import Dashboard from "./Components/Dashboard";
import ProtectedRoute from "./Components/AuthenticationComponents/ProtectedRoute";
import SplashScreen from "./Components/SplashScreen";

function App() {
  function Logout() {
    return;
  }

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
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;

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
import Dashboard from "./Features/Dashboard/Components/DashboardComponent";
import Users from "./Features/Users/Components/UsersComponent";
import Employees from "./Features/Employees/Components/EmployeeCore/EmployeeComponent";
import AllUsersComponent from "./Features/Users/Components/AllUsersComponent";
import AddUsersComponent from "./Features/Users/Components/AddUsersComponent";
import UpdateUser from "./Features/Users/Components/UpdateUserComponent";
import SampleEmployees from "./Features/Employees/Components/EmployeeCore/SampleEmployeesComponent";
import EmployeeDashboard from "./Features/Employees/Components/EmployeeCore/EmployeeDashboardComponent";
import EmployeeOccurrence from "./Features/Employees/Components/Occurrence/EmployeeOccurrenceComponent";
import EmployeePrimary from "./Features/Employees/Components/Primary/EmployeePrimaryComponent";
import ListOccurrence from "./Features/Employees/Components/Occurrence/ListOccurrenceComponent";
import EditOccurrence from "./Features/Employees/Components/Occurrence/EditOccurrenceComponent";
import AddOccurrence from "./Features/Employees/Components/Occurrence/AddOccurrenceComponent";
import EmployeeChildren from "./Features/Employees/Components/Children/EmployeeChildrenComponent";
import ListChildren from "./Features/Employees/Components/Children/ListChildrenComponent";
import EditChildren from "./Features/Employees/Components/Children/EditChildrenComponent";
import AddChildren from "./Features/Employees/Components/Children/AddChildrenComponent";

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
          path="/home"
          element={
            <ProtectedRoute>
              <HomePage />
            </ProtectedRoute>
          }
        >
          <Route index element={<Dashboard />} />
          <Route path="users" element={<Users />}>
            <Route index element={<AllUsersComponent />} />
            <Route path="all" element={<AllUsersComponent />} />
            <Route path="add" element={<AddUsersComponent />} />
            <Route path="update/:id" element={<UpdateUser />} />
          </Route>
          <Route path="employees" element={<Employees />}>
            <Route index element={<SampleEmployees />} />
            <Route path=":serviceId" element={<EmployeeDashboard />}>
              <Route index element={<EmployeePrimary />} />
              <Route path="occurrence" element={<EmployeeOccurrence />}>
                <Route index element={<ListOccurrence />} />
                <Route path="add/" element={<AddOccurrence />} />
                <Route path="edit/:occurrenceId" element={<EditOccurrence />} />
              </Route>
              <Route path="children" element={<EmployeeChildren />}>
                <Route index element={<ListChildren />} />
                <Route path="add/" element={<AddChildren />} />
                <Route path="edit/:childId" element={<EditChildren />} />
              </Route>
            </Route>
          </Route>
        </Route>
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

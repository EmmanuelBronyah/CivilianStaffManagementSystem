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
import EmployeeCourses from "./Features/Employees/Components/Courses/EmployeeCoursesComponent";
import ListCourses from "./Features/Employees/Components/Courses/ListCoursesComponent";
import EditCourses from "./Features/Employees/Components/Courses/EditCoursesComponent";
import AddCourses from "./Features/Employees/Components/Courses/AddCoursesComponent";
import EmployeeAbsences from "./Features/Employees/Components/Absences/EmployeeAbsencesComponent";
import ListAbsences from "./Features/Employees/Components/Absences/ListAbsencesComponent";
import EditAbsences from "./Features/Employees/Components/Absences/EditAbsencesComponent";
import AddAbsences from "./Features/Employees/Components/Absences/AddAbsencesComponent";
import EmployeeNextOfKin from "./Features/Employees/Components/Next Of Kin/EmployeeNextOfKinComponent";
import ListNextOfKin from "./Features/Employees/Components/Next Of Kin/ListNextOfKinComponent";
import EditNextOfKin from "./Features/Employees/Components/Next Of Kin/EditNextOfKinComponent";
import AddNextOfKin from "./Features/Employees/Components/Next Of Kin/AddNextOfKinComponent";
import EmployeeSpouse from "./Features/Employees/Components/Spouse/EmployeeSpouseComponent";
import ListSpouse from "./Features/Employees/Components/Spouse/ListSpouseComponent";
import EditSpouse from "./Features/Employees/Components/Spouse/EditSpouseComponent";
import AddSpouse from "./Features/Employees/Components/Spouse/AddSpouseComponent";
import EmployeeTermination from "./Features/Employees/Components/Termination Of Appointment/EmployeeTerminationComponent";
import ListTermination from "./Features/Employees/Components/Termination Of Appointment/ListTerminationComponent";
import AddTermination from "./Features/Employees/Components/Termination Of Appointment/AddTerminationComponent";
import EditTermination from "./Features/Employees/Components/Termination Of Appointment/EditTerminationComponent";
import ListIdentity from "./Features/Employees/Components/Identity/ListIdentityComponent";
import EmployeeIdentity from "./Features/Employees/Components/Identity/EmployeeIdentityComponent";
import AddIdentity from "./Features/Employees/Components/Identity/AddIdentityComponent";
import EditIdentity from "./Features/Employees/Components/Identity/EditIdentityComponent";
import ListServiceWithForces from "./Features/Employees/Components/Service With Forces/ListServiceWithForcesComponent";
import EmployeeServiceWithForces from "./Features/Employees/Components/Service With Forces/EmployeeServiceWithForcesComponent";
import AddService from "./Features/Employees/Components/Service With Forces/AddServiceComponent";
import EditService from "./Features/Employees/Components/Service With Forces/EditServiceWithForcesComponent";
import EmployeePreviousGovernmentService from "./Features/Employees/Components/Previous Government Service/EmployeePreviousGovernmentServiceComponent";
import ListPreviousGovernmentService from "./Features/Employees/Components/Previous Government Service/ListPreviousGovernmentServiceComponent";
import AddPreviousGovernmentService from "./Features/Employees/Components/Previous Government Service/AddPreviousGovernmentServiceComponent";
import EditPreviousGovernmentService from "./Features/Employees/Components/Previous Government Service/EditPreviousGovernmentServiceComponent";

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
          {/* DASHBOARD */}
          <Route index element={<Dashboard />} />

          {/* USERS */}
          <Route path="users" element={<Users />}>
            <Route index element={<AllUsersComponent />} />
            <Route path="all" element={<AllUsersComponent />} />
            <Route path="add" element={<AddUsersComponent />} />
            <Route path="update/:id" element={<UpdateUser />} />
          </Route>

          {/* EMPLOYEES */}
          <Route path="employees" element={<Employees />}>
            <Route index element={<SampleEmployees />} />
            <Route path=":serviceId" element={<EmployeeDashboard />}>
              {/* PRIMARY */}
              <Route index element={<EmployeePrimary />} />
              {/* OCCURRENCE */}
              <Route path="occurrence" element={<EmployeeOccurrence />}>
                <Route index element={<ListOccurrence />} />
                <Route path="add/" element={<AddOccurrence />} />
                <Route path="edit/:occurrenceId" element={<EditOccurrence />} />
              </Route>
              {/* CHILDREN */}
              <Route path="children" element={<EmployeeChildren />}>
                <Route index element={<ListChildren />} />
                <Route path="add/" element={<AddChildren />} />
                <Route path="edit/:childId" element={<EditChildren />} />
              </Route>
              {/* COURSES */}
              <Route path="courses" element={<EmployeeCourses />}>
                <Route index element={<ListCourses />} />
                <Route path="add/" element={<AddCourses />} />
                <Route path="edit/:courseId" element={<EditCourses />} />
              </Route>
              {/* ABSENCES */}
              <Route path="absences" element={<EmployeeAbsences />}>
                <Route index element={<ListAbsences />} />
                <Route path="add/" element={<AddAbsences />} />
                <Route path="edit/:absencesId" element={<EditAbsences />} />
              </Route>
              {/* NEXT OF KIN */}
              <Route path="nextOfKin" element={<EmployeeNextOfKin />}>
                <Route index element={<ListNextOfKin />} />
                <Route path="add/" element={<AddNextOfKin />} />
                <Route path="edit/:nextOfKinId" element={<EditNextOfKin />} />
              </Route>
              {/* SPOUSE */}
              <Route path="spouse" element={<EmployeeSpouse />}>
                <Route index element={<ListSpouse />} />
                <Route path="add/" element={<AddSpouse />} />
                <Route path="edit/:spouseId" element={<EditSpouse />} />
              </Route>
              {/* TERMINATION OF APPOINTMENT */}
              <Route path="termination" element={<EmployeeTermination />}>
                <Route index element={<ListTermination />} />
                <Route path="add/" element={<AddTermination />} />
                <Route
                  path="edit/:terminationId"
                  element={<EditTermination />}
                />
              </Route>
              {/* IDENTITY */}
              <Route path="identity" element={<EmployeeIdentity />}>
                <Route index element={<ListIdentity />} />
                <Route path="add/" element={<AddIdentity />} />
                <Route path="edit/:identityId" element={<EditIdentity />} />
              </Route>
              {/* SERVICE WITH FORCES */}
              <Route
                path="serviceWithForces"
                element={<EmployeeServiceWithForces />}
              >
                <Route index element={<ListServiceWithForces />} />
                <Route path="add/" element={<AddService />} />
                <Route
                  path="edit/:serviceWithForcesId"
                  element={<EditService />}
                />
              </Route>
              {/* PREVIOUS GOVERNMENT SERVICE */}
              <Route
                path="previousGovernmentService"
                element={<EmployeePreviousGovernmentService />}
              >
                <Route index element={<ListPreviousGovernmentService />} />
                <Route path="add/" element={<AddPreviousGovernmentService />} />
                <Route
                  path="edit/:previousGovernmentServiceId"
                  element={<EditPreviousGovernmentService />}
                />
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

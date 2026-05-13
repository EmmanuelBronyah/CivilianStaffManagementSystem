import { Outlet, useOutletContext } from "react-router-dom";

export default function EmployeeCourses() {
  const { setResponse } = useOutletContext();

  return <Outlet context={{ setResponse }} />;
}

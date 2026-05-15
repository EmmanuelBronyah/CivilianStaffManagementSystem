import { Outlet, useOutletContext } from "react-router-dom";

export default function EmployeeServiceWithForces() {
  const { setResponse } = useOutletContext();

  return <Outlet context={{ setResponse }} />;
}

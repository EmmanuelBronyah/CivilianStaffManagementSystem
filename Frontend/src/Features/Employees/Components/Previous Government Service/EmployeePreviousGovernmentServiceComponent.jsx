import { Outlet, useOutletContext } from "react-router-dom";

export default function EmployeePreviousGovernmentService() {
  const { setResponse } = useOutletContext();

  return <Outlet context={{ setResponse }} />;
}

import { Outlet, useOutletContext } from "react-router-dom";

export default function EmployeeTermination() {
  const { setResponse } = useOutletContext();

  return <Outlet context={{ setResponse }} />;
}

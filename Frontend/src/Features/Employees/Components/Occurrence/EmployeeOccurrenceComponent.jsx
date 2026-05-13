import { Outlet, useOutletContext } from "react-router-dom";

export default function EmployeeOccurrence() {
  const { setResponse } = useOutletContext();

  return <Outlet context={{ setResponse }} />;
}

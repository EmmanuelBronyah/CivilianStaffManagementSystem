import { Outlet, useOutletContext } from "react-router-dom";

export default function EmployeeIdentity() {
  const { setResponse } = useOutletContext();

  return <Outlet context={{ setResponse }} />;
}

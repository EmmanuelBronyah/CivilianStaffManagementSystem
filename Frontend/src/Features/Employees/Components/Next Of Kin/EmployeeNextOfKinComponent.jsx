import { Outlet, useOutletContext } from "react-router-dom";

export default function EmployeeNextOfKin() {
  const { setResponse } = useOutletContext();

  return <Outlet context={{ setResponse }} />;
}

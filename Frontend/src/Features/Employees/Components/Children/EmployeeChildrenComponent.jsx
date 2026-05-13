import { Outlet, useOutletContext } from "react-router-dom";

export default function EmployeeChildren() {
  const { setResponse } = useOutletContext();

  return <Outlet context={{ setResponse }} />;
}

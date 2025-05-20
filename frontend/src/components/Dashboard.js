import React, { useState } from "react";

const sampleMachines = [
  {
    id: 1,
    name: "Machine A",
    os: "Ubuntu 20.04",
    lastCheckIn: "2025-05-19 14:20",
    encryptedDisk: true,
    outdatedOS: false,
  },
  {
    id: 2,
    name: "Machine B",
    os: "Windows 10",
    lastCheckIn: "2025-05-19 14:15",
    encryptedDisk: false,
    outdatedOS: true,
  },
];

function Dashboard() {
  const [machines] = useState(sampleMachines);

  return (
    <div>
      <h2>Reporting Machines</h2>
      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>Name</th>
            <th>OS</th>
            <th>Last Check-In</th>
            <th>Encrypted Disk</th>
            <th>Outdated OS</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {machines.map((machine) => (
            <tr key={machine.id}>
              <td>{machine.name}</td>
              <td>{machine.os}</td>
              <td>{machine.lastCheckIn}</td>
              <td>{machine.encryptedDisk ? "✅" : "❌"}</td>
              <td>{machine.outdatedOS ? "❌" : "✅"}</td>
              <td>
                {machine.encryptedDisk && !machine.outdatedOS
                  ? "✅ Healthy"
                  : "⚠️ Issue"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Dashboard;

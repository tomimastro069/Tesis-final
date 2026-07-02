import React, { useEffect, useRef } from "react";
import { useScan } from "../context/ScanContext";

export function MSDOSPrompt() {
  const { terminalLogs } = useScan();
  const bottomRef = useRef<HTMLDivElement>(null);

  // Auto scroll al final de los logs
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [terminalLogs]);

  return (
    <div className="bg-black text-[#00ff00] font-mono text-[11px] p-2 flex-1 min-h-0 overflow-y-auto selection:bg-[#00ff00] selection:text-black">
      <div>Microsoft(R) Windows 98</div>
      <div>(C)Copyright Microsoft Corp 1981-1998.</div>
      <div className="mb-2"></div>
      
      <div className="flex flex-col gap-1">
        {terminalLogs.map((log, index) => (
          <div key={index} className="whitespace-pre-wrap break-all leading-tight">
            {log}
          </div>
        ))}
      </div>
      
      <div ref={bottomRef} className="mt-1 flex items-center gap-1">
        <span>C:\WINDOWS&gt;</span>
        <span className="w-1.5 h-3 bg-[#00ff00] animate-[ping_1s_infinite]"></span>
      </div>
    </div>
  );
}

import React, { useEffect, useRef, useState } from "react";
import { useScan } from "../context/ScanContext";

export function MSDOSPrompt() {
  const { terminalLogs, activeScan, cancelActiveScan } = useScan();
  const bottomRef = useRef<HTMLDivElement>(null);
  const [cancelling, setCancelling] = useState(false);

  // Auto scroll al final de los logs
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [terminalLogs]);

  const handleCancel = async () => {
    if (!confirm("¿Cancelar el análisis activo? Si quedó trabado (por ejemplo, tras reiniciar el backend), esto lo descarta para que puedas iniciar uno nuevo.")) {
      return;
    }
    setCancelling(true);
    try {
      await cancelActiveScan();
    } finally {
      setCancelling(false);
    }
  };

  return (
    <div className="bg-black text-[#00ff00] font-mono text-[11px] flex-1 min-h-0 flex flex-col">
      <div className="flex-1 min-h-0 overflow-y-auto p-2 selection:bg-[#00ff00] selection:text-black">
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

      {activeScan && (
        <div className="flex-shrink-0 bg-[#c0c0c0] border-t-2 border-white px-2 py-1 flex items-center justify-between font-win98 text-black">
          <span className="text-[10px]">
            Análisis activo: {activeScan.target}
            {activeScan.progressMessage ? ` — ${activeScan.progressMessage}` : ""}
          </span>
          <button
            onClick={handleCancel}
            disabled={cancelling}
            title="Si el backend se reinició o el análisis quedó trabado, esto lo descarta para poder iniciar uno nuevo."
            className="px-2 py-[1px] text-[11px] win98-border active:win98-border-inset bg-[#c0c0c0] text-[#800000] font-bold disabled:text-gray-500"
          >
            {cancelling ? "Cancelando..." : "Cancelar Análisis"}
          </button>
        </div>
      )}
    </div>
  );
}

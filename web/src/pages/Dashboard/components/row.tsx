export function TableRow({ children }: { children: React.ReactNode }) {
  return (
    <tr
      className={[
        "z-10",
        "border-b transition-colors",
        "bg-white",
        "hover:bg-slate-200",
        "hover:last:text-green-500",
        "group",
        "font-medium",
      ].join(" ")}
    >
      {children}
    </tr>
  );
}

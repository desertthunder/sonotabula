export function TableRow({ children }: { children: React.ReactNode }) {
  return (
    <tr
      className={[
        "z-10",
        "border-b transition-colors",
        "bg-white",
        "hover:bg-slate-200",
        "even:bg-slate-100",
        "hover:last:text-green-500",
        "group",
      ].join(" ")}
    >
      {children}
    </tr>
  );
}

import clsx from "clsx";

interface StatusBadgeProps {
  status: "confirmed" | "pending" | "cancelled";
}

const STATUS_COLORS: Record<StatusBadgeProps["status"], string> = {
  confirmed: "bg-emerald-100 text-emerald-700",
  pending: "bg-amber-100 text-amber-700",
  cancelled: "bg-rose-100 text-rose-700"
};

const StatusBadge = ({ status }: StatusBadgeProps) => {
  return <span className={clsx("px-2 py-1 rounded-full text-xs font-medium", STATUS_COLORS[status])}>{status}</span>;
};

export default StatusBadge;

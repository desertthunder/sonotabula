import { Library } from "./Library";
import { COUNT_KEYS } from "@/libs/types/api";
import { StatCard } from "./components/Stats";
import { Text, Box, Flex } from "@radix-ui/themes";

export function Dashboard() {
  return (
    <Flex
      flexGrow="1"
      gap="8"
      justify="between"
      className="px-8 pt-4" //bg-gradient-to-b from-emerald-600 to-50% via-emerald-500 via-50%"
    >
      <Flex direction="column" gap="4">
        <h1 className="text-base font-semibold text-zinc-100">Dashboard</h1>
        <Text className="text-sm text-zinc-100">
          View your stats and library at a glance.
        </Text>
        <Box flexGrow="1">
          <Library />
        </Box>
      </Flex>

      <Flex direction="column" minWidth="20%" gap="4">
        {COUNT_KEYS.map((key) => (
          <StatCard key={key} scope={key} />
        ))}
      </Flex>
    </Flex>
  );
}

export { DashboardLayout } from "./Layout";

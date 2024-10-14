import { Flex, TextField } from "@radix-ui/themes";
import { Link } from "react-router-dom";

export function Navbar() {
  return (
    <Flex
      className="border-b-4 border-green-500 px-4 pr-8 py-1 bg-white"
      justify="between"
    >
      <Link
        to="/"
        className="text-lg text-black flex items-center hover:text-green-500"
      >
        <i className="i-ri-spotify-line text-xl  mr-1" />
        <span>Dashspot</span>
      </Link>
      <TextField.Root
        placeholder="Search"
        style={{
          minWidth: "20%",
        }}
      >
        <TextField.Slot>
          <span className="i-ri-search-2-line w-4 h-4" />
        </TextField.Slot>
      </TextField.Root>
    </Flex>
  );
}

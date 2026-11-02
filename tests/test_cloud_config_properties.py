"""Checks that the Spring Cloud Config property files parse and keep their values."""

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = REPO_ROOT / "cloud-config-repo"


def load_properties(path):
    """Load a Java .properties file, including ':' separators and backslash escapes."""
    values = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or line.startswith("!"):
            continue
        key, value = _split_property(line)
        values[key] = _unescape(value)
    return values


def _split_property(line):
    escaped = False
    for index, char in enumerate(line):
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char in "=:" or char.isspace():
            key = line[:index]
            rest = line[index + 1 :]
            if char.isspace():
                rest = rest.lstrip()
                if rest[:1] in "=:":
                    rest = rest[1:]
            return _unescape(key), rest.lstrip(" \t")
    return _unescape(line), ""


def _unescape(text):
    result = []
    index = 0
    while index < len(text):
        char = text[index]
        if char != "\\":
            result.append(char)
            index += 1
            continue
        index += 1
        if index >= len(text):
            break
        escaped = text[index]
        result.append(
            {
                "n": "\n",
                "r": "\r",
                "t": "\t",
            }.get(escaped, escaped)
        )
        index += 1
    return "".join(result)


class CloudConfigPropertiesTest(unittest.TestCase):
    def test_dev_profile_exposes_datasource_and_logging(self):
        props = load_properties(CONFIG_DIR / "cloud-config-dev.properties")

        self.assertEqual(
            props["mysqldb.datasource.url"],
            "jdbc:mysql://localhost:3306/test?useUnicode=true&characterEncoding=utf-8",
        )
        self.assertEqual(props["mysqldb.datasource.username"], "root")
        self.assertEqual(props["mysqldb.datasource.password"], "123qwe")
        self.assertEqual(props["logging.level.org.springframework.web"], "DEBUG")

    def test_test_profile_adds_message_without_dropping_shared_settings(self):
        dev = load_properties(CONFIG_DIR / "cloud-config-dev.properties")
        test = load_properties(CONFIG_DIR / "cloud-config-test.properties")

        for key in (
            "mysqldb.datasource.url",
            "mysqldb.datasource.username",
            "mysqldb.datasource.password",
            "logging.level.org.springframework.web",
        ):
            self.assertEqual(test[key], dev[key])
        self.assertEqual(test["mymsg"], "zhangzh")

    def test_service_names(self):
        compute = load_properties(CONFIG_DIR / "compute-service-dev.properties")
        client = load_properties(CONFIG_DIR / "config-client-test.properties")

        self.assertEqual(compute["name"], "zhangzhaohui")
        self.assertEqual(client["name"], "zhangzh")


if __name__ == "__main__":
    unittest.main()

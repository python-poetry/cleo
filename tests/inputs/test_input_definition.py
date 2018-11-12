# -*- coding: utf-8 -*-

from cleo.inputs import InputDefinition, InputArgument, InputOption

from .. import CleoTestCase


class InputDefinitionTest(CleoTestCase):
    def setUp(self):
        super(InputDefinitionTest, self).setUp()

        self.foo = None
        self.bar = None
        self.foo1 = None
        self.foo2 = None

    def test_init_arguments(self):
        self.initialize_arguments()

        definition = InputDefinition()
        self.assertEqual([], definition.get_arguments())

        definition = InputDefinition([self.foo, self.bar])
        self.assertEqual([self.foo, self.bar], definition.get_arguments())

    def test_init_options(self):
        self.initialize_options()

        definition = InputDefinition()
        self.assertEqual([], definition.get_options())

        definition = InputDefinition([self.foo, self.bar])
        self.assertEqual([self.foo, self.bar], definition.get_options())

    def test_set_arguments(self):
        self.initialize_arguments()

        definition = InputDefinition()
        definition.set_arguments([self.foo])
        self.assertEqual([self.foo], definition.get_arguments())
        definition.set_arguments([self.bar])
        self.assertEqual([self.bar], definition.get_arguments())

    def test_add_arguments(self):
        self.initialize_arguments()

        definition = InputDefinition()
        definition.add_arguments([self.foo])
        self.assertEqual([self.foo], definition.get_arguments())
        definition.add_arguments([self.bar])
        self.assertEqual([self.foo, self.bar], definition.get_arguments())

    def test_add_argument(self):
        self.initialize_arguments()

        definition = InputDefinition()
        definition.add_argument(self.foo)
        self.assertEqual([self.foo], definition.get_arguments())
        definition.add_argument(self.bar)
        self.assertEqual([self.foo, self.bar], definition.get_arguments())

    def test_arguments_must_have_different_names(self):
        self.initialize_arguments()

        definition = InputDefinition()
        definition.add_argument(self.foo)
        self.assertRaisesRegexp(
            Exception,
            'An argument with name "foo" already exists.',
            definition.add_argument,
            self.foo1,
        )

    def test_list_argument_has_to_be_last(self):
        self.initialize_arguments()

        definition = InputDefinition()
        definition.add_argument(InputArgument("foolist", InputArgument.IS_LIST))
        self.assertRaisesRegexp(
            Exception,
            "Cannot add an argument after a list argument.",
            definition.add_argument,
            InputArgument("anotherbar"),
        )

    def test_required_argument_cannot_follow_an_optional_one(self):
        self.initialize_arguments()

        definition = InputDefinition()
        definition.add_argument(self.foo)
        self.assertRaisesRegexp(
            Exception,
            "Cannot add a required argument after an optional one.",
            definition.add_argument,
            self.foo2,
        )

    def test_get_argument(self):
        self.initialize_arguments()

        definition = InputDefinition()
        definition.add_arguments([self.foo])
        self.assertEqual(self.foo, definition.get_argument("foo"))

    def test_get_invalid_argument(self):
        self.initialize_arguments()

        definition = InputDefinition()
        definition.add_arguments([self.foo])
        self.assertRaises(
            Exception,
            'The "bar" argument does not exist.',
            definition.get_argument,
            "bar",
        )

    def test_has_argument(self):
        self.initialize_arguments()

        definition = InputDefinition()
        definition.add_arguments([self.foo])

        self.assertTrue(definition.has_argument("foo"))
        self.assertFalse(definition.has_argument("bar"))

    def test_get_argument_required_count(self):
        self.initialize_arguments()

        definition = InputDefinition()
        definition.add_argument(self.foo2)
        self.assertEqual(1, definition.get_argument_required_count())
        definition.add_argument(self.foo)
        self.assertEqual(1, definition.get_argument_required_count())

    def test_argument_count(self):
        self.initialize_arguments()

        definition = InputDefinition()
        definition.add_argument(self.foo2)
        self.assertEqual(1, definition.get_argument_count())
        definition.add_argument(self.foo)
        self.assertEqual(2, definition.get_argument_count())

    def test_get_argument_default(self):
        definition = InputDefinition(
            [
                InputArgument("foo1", InputArgument.OPTIONAL),
                InputArgument("foo2", InputArgument.OPTIONAL, "", "default"),
                InputArgument("foo3", InputArgument.OPTIONAL | InputArgument.IS_LIST),
            ]
        )
        self.assertEqual(
            {"foo1": None, "foo2": "default", "foo3": []},
            definition.get_argument_defaults(),
        )

        definition = InputDefinition(
            [
                InputArgument(
                    "foo4", InputArgument.OPTIONAL | InputArgument.IS_LIST, "", [1, 2]
                )
            ]
        )
        self.assertEqual({"foo4": [1, 2]}, definition.get_argument_defaults())

    def test_set_options(self):
        self.initialize_options()

        definition = InputDefinition([self.foo])
        self.assertEqual([self.foo], definition.get_options())
        definition.set_options([self.bar])
        self.assertEqual([self.bar], definition.get_options())

    def test_set_options_clears_options(self):
        self.initialize_options()

        definition = InputDefinition([self.foo])
        definition.set_options([self.bar])
        self.assertRaisesRegexp(
            Exception,
            'The "-f" option does not exist.',
            definition.get_option_for_shortcut,
            "f",
        )

    def test_add_options(self):
        self.initialize_options()

        definition = InputDefinition([self.foo])
        self.assertEqual([self.foo], definition.get_options())
        definition.add_options([self.bar])
        self.assertEqual([self.foo, self.bar], definition.get_options())

    def test_add_option(self):
        self.initialize_options()

        definition = InputDefinition()
        definition.add_option(self.foo)
        self.assertEqual([self.foo], definition.get_options())
        definition.add_option(self.bar)
        self.assertEqual([self.foo, self.bar], definition.get_options())

    def test_add_duplicate_option(self):
        self.initialize_options()

        definition = InputDefinition()
        definition.add_option(self.foo)
        self.assertRaisesRegexp(
            Exception,
            'An option named "foo" already exists.',
            definition.add_option,
            self.foo2,
        )

    def test_add_duplicate_shortcut_option(self):
        self.initialize_options()

        definition = InputDefinition()
        definition.add_option(self.foo)
        self.assertRaisesRegexp(
            Exception,
            'An option with shortcut "f" already exists.',
            definition.add_option,
            self.foo1,
        )

    def test_get_option(self):
        self.initialize_options()

        definition = InputDefinition([self.foo])
        self.assertEqual(self.foo, definition.get_option("foo"))

    def test_get_invalid_option(self):
        self.initialize_options()

        definition = InputDefinition([self.foo])
        self.assertRaisesRegexp(
            Exception,
            'The "--bar" option does not exist.',
            definition.get_option,
            "bar",
        )

    def test_has_option(self):
        self.initialize_options()

        definition = InputDefinition([self.foo])
        self.assertTrue(definition.has_option("foo"))
        self.assertFalse(definition.has_option("bar"))

    def test_has_shortcut(self):
        self.initialize_options()

        definition = InputDefinition([self.foo])
        self.assertTrue(definition.has_shortcut("f"))
        self.assertFalse(definition.has_shortcut("b"))

    def test_get_option_for_shortcut(self):
        self.initialize_options()

        definition = InputDefinition([self.foo])
        self.assertEqual(self.foo, definition.get_option_for_shortcut("f"))

    def test_get_option_for_multi_shortcut(self):
        self.initialize_options()

        definition = InputDefinition([self.multi])
        self.assertEqual(self.multi, definition.get_option_for_shortcut("m"))
        self.assertEqual(self.multi, definition.get_option_for_shortcut("mmm"))

    def test_get_options_defaults(self):
        definition = InputDefinition(
            [
                InputOption("foo1", None, InputOption.VALUE_NONE),
                InputOption("foo2", None, InputOption.VALUE_REQUIRED),
                InputOption("foo3", None, InputOption.VALUE_REQUIRED, "", "default"),
                InputOption("foo4", None, InputOption.VALUE_OPTIONAL),
                InputOption("foo5", None, InputOption.VALUE_OPTIONAL, "", "default"),
                InputOption(
                    "foo6", None, InputOption.VALUE_OPTIONAL | InputOption.VALUE_IS_LIST
                ),
                InputOption(
                    "foo7",
                    None,
                    InputOption.VALUE_OPTIONAL | InputOption.VALUE_IS_LIST,
                    "",
                    [1, 2],
                ),
            ]
        )
        defaults = {
            "foo1": False,
            "foo2": None,
            "foo3": "default",
            "foo4": None,
            "foo5": "default",
            "foo6": [],
            "foo7": [1, 2],
        }

        self.assertEqual(defaults, definition.get_option_defaults())

    def test_get_synopsis(self):
        definition = InputDefinition([InputOption("foo")])
        self.assertEqual("[--foo]", definition.get_synopsis())
        definition = InputDefinition([InputOption("foo", "f")])
        self.assertEqual("[-f|--foo]", definition.get_synopsis())
        definition = InputDefinition(
            [InputOption("foo", "f", InputOption.VALUE_REQUIRED)]
        )
        self.assertEqual("[-f|--foo FOO]", definition.get_synopsis())
        definition = InputDefinition(
            [InputOption("foo", "f", InputOption.VALUE_OPTIONAL)]
        )
        self.assertEqual("[-f|--foo [FOO]]", definition.get_synopsis())

        definition = InputDefinition([InputArgument("foo")])
        self.assertEqual("[<foo>]", definition.get_synopsis())
        definition = InputDefinition([InputArgument("foo", InputArgument.REQUIRED)])
        self.assertEqual("<foo>", definition.get_synopsis())
        definition = InputDefinition([InputArgument("foo", InputArgument.IS_LIST)])
        self.assertEqual("[<foo>]...", definition.get_synopsis())
        definition = InputDefinition(
            [InputArgument("foo", InputArgument.REQUIRED | InputArgument.IS_LIST)]
        )
        self.assertEqual("<foo> (<foo>)...", definition.get_synopsis())

    def initialize_arguments(self):
        self.foo = InputArgument("foo")
        self.bar = InputArgument("bar")
        self.foo1 = InputArgument("foo")
        self.foo2 = InputArgument("foo2", InputArgument.REQUIRED)

    def initialize_options(self):
        self.foo = InputOption("foo", "f")
        self.bar = InputOption("bar", "b")
        self.foo1 = InputOption("fooBis", "f")
        self.foo2 = InputOption("foo", "p")
        self.multi = InputOption("multi", "m|mm|mmm")

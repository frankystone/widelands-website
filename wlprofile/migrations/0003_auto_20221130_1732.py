# Generated by Django 2.2.28 on 2022-11-30 17:32

from django.db import migrations, models
import django.db.models.deletion
import wlprofile.fields


class Migration(migrations.Migration):

    dependencies = [
        ("wlhelp", "0003_auto_20221129_2035"),
        ("wlprofile", "0002_profile_deleted"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="aim",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="icq",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="jabber",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="msn",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="site",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="yahoo",
        ),
        migrations.AddField(
            model_name="profile",
            name="favourite_addon",
            field=models.CharField(
                blank=True,
                default="",
                max_length=255,
                verbose_name="Your favourite Add-On",
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="favourite_map",
            field=models.CharField(
                blank=True,
                default="",
                max_length=100,
                verbose_name="Your favourite Map(s)",
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="favourite_tribe",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="wlhelp.Tribe",
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="operating_system",
            field=models.CharField(
                blank=True, default="", max_length=100, verbose_name="Operating System"
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="webservice_nick",
            field=models.CharField(
                blank=True, default="", max_length=255, verbose_name="Webservice/Nick"
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="widelands_version",
            field=models.CharField(
                blank=True, default="", max_length=255, verbose_name="Widelands Version"
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="avatar",
            field=wlprofile.fields.ExtendedImageField(
                blank=True,
                default="wlprofile/anonymous.png",
                upload_to="wlprofile/avatars/",
                verbose_name="Avatar",
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="location",
            field=models.CharField(
                blank=True, default="", max_length=30, verbose_name="Location"
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="show_signatures",
            field=models.BooleanField(
                blank=True, default=True, verbose_name="Show signatures"
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="signature",
            field=models.TextField(
                blank=True, default="", max_length=255, verbose_name="Signature"
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="time_display",
            field=models.CharField(
                default="%ND(Y-m-d,) H:i", max_length=80, verbose_name="Time display"
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="time_zone",
            field=models.FloatField(
                choices=[
                    (-12.0, "-12"),
                    (-11.0, "-11"),
                    (-10.0, "-10"),
                    (-9.5, "-09.5"),
                    (-9.0, "-09"),
                    (-8.5, "-08.5"),
                    (-8.0, "-08 PST"),
                    (-7.0, "-07 MST"),
                    (-6.0, "-06 CST"),
                    (-5.0, "-05 EST"),
                    (-4.0, "-04 AST"),
                    (-3.5, "-03.5"),
                    (-3.0, "-03 ADT"),
                    (-2.0, "-02"),
                    (-1.0, "-01"),
                    (0.0, "00 GMT"),
                    (1.0, "+01 CET"),
                    (2.0, "+02"),
                    (3.0, "+03"),
                    (3.5, "+03.5"),
                    (4.0, "+04"),
                    (4.5, "+04.5"),
                    (5.0, "+05"),
                    (5.5, "+05.5"),
                    (6.0, "+06"),
                    (6.5, "+06.5"),
                    (7.0, "+07"),
                    (8.0, "+08"),
                    (9.0, "+09"),
                    (9.5, "+09.5"),
                    (10.0, "+10"),
                    (10.5, "+10.5"),
                    (11.0, "+11"),
                    (11.5, "+11.5"),
                    (12.0, "+12"),
                    (13.0, "+13"),
                    (14.0, "+14"),
                ],
                default=3.0,
                verbose_name="Time zone",
            ),
        ),
    ]

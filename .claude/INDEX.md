# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
 10338  GET              /                                                dashboard
 12393  GET              /api/abo/status                                  api_abo_status
 12347  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 11126  GET              /api/automation/status                           api_automation_status
 11148  POST             /api/automation/toggle                           api_automation_toggle
 20451  GET              /api/channel/categories                          api_channel_categories
 20457  POST             /api/channel/set                                 api_channel_set
 20304  GET              /api/channels/status                             api_channels_status
 19978  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 19961  GET              /api/clips                                       api_clips
 20007  POST/DELETE      /api/clips/clear                                 api_clips_clear
 19879  GET              /api/debug/threads                               api_debug_threads
 12358  GET              /api/events                                      api_events
 11837  GET              /api/events/stream                               api_events_stream
 11664  GET              /api/health                                      api_health
 19920  POST             /api/highlights/config                           api_highlights_config
 10268  POST             /api/login                                       dashboard_login_submit
 12683  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 11752  GET              /api/notify/status                               api_notify_status
 11763  POST             /api/notify/test                                 api_notify_test
 12447  GET              /api/proxy/heatmap                               api_proxy_heatmap
 12424  GET              /api/proxy/trend                                 api_proxy_trend
 20027  GET              /api/tts/<fn>                                    api_tts_file
 20804  GET              /api/upload_window                               api_upload_window
 11954  GET              /archive/<int:eid>/download                      archive_download
 11982  GET              /download/<int:recording_id>                     download
 11911  GET              /health                                          health
 19788  GET              /healthz                                         healthz
 10259  GET              /login                                           dashboard_login_page
 10293  GET              /logout                                          dashboard_logout
 10300  GET              /manifest.webmanifest                            pwa_manifest
 20777  GET              /overlay                                         overlay_page
 10324  GET              /pwa-icon-<variant>.png                          pwa_icon
 10310  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (345)

```
   195  GET              /api/active-recordings                           api_active_recordings   [nc/routes/auskunft.py]
   422  GET              /api/activity-pulse                              api_activity_pulse   [nc/routes/auskunft.py]
   195  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   165  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
   993  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   738  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   864  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   844  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   882  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   806  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   356  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   367  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   377  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   400  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   407  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   418  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   546  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   644  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1231  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1263  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   341  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   946  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   926  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1099  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1147  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1198  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1057  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   901  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   504  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   768  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   650  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   633  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   625  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   456  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   472  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   812  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   374  GET              /api/archive/scan                                api_archive_scan   [nc/routes/archive.py]
   405  POST             /api/archive/scan/adopt                          api_archive_scan_adopt   [nc/routes/archive.py]
   777  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   797  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   684  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    49  GET/POST         /api/audio/config                                api_audio_config   [nc/routes/audio.py]
    78  POST             /api/audio/testtone                              api_audio_testtone   [nc/routes/audio.py]
   238  GET/POST         /api/auto-archive-rules                          api_archive_rules   [nc/routes/wartung.py]
   263  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete   [nc/routes/wartung.py]
   268  POST             /api/auto-archive-rules/run                      api_archive_rules_run   [nc/routes/wartung.py]
   163  GET              /api/azrael/agents                               api_azrael_agents   [nc/routes/azrael.py]
    99  POST             /api/azrael/ask                                  api_azrael_ask   [nc/routes/azrael.py]
   222  GET/POST         /api/azrael/context                              api_azrael_context   [nc/routes/azrael.py]
   120  GET              /api/azrael/core                                 api_azrael_core   [nc/routes/azrael.py]
   342  POST             /api/azrael/live_pause                           api_azrael_live_pause   [nc/routes/azrael.py]
   328  GET              /api/azrael/live_status                          api_azrael_live_status   [nc/routes/azrael.py]
   350  POST             /api/azrael/live_test                            api_azrael_live_test   [nc/routes/azrael.py]
   174  GET              /api/azrael/memories                             api_azrael_memories   [nc/routes/azrael.py]
   406  POST             /api/azrael/persona                              api_azrael_persona_set   [nc/routes/azrael.py]
   397  GET              /api/azrael/personas                             api_azrael_personas   [nc/routes/azrael.py]
   314  GET              /api/azrael/piper_status                         api_azrael_piper_status   [nc/routes/azrael.py]
   190  POST             /api/azrael/react                                api_azrael_react   [nc/routes/azrael.py]
   231  GET              /api/azrael/reaction                             api_azrael_reaction   [nc/routes/azrael.py]
   243  GET              /api/azrael/reactions                            api_azrael_reactions   [nc/routes/azrael.py]
   372  GET              /api/azrael/transcript                           api_azrael_transcript   [nc/routes/azrael.py]
   281  POST             /api/azrael/tts_test                             api_azrael_tts_test   [nc/routes/azrael.py]
   267  GET              /api/azrael/voices                               api_azrael_voices   [nc/routes/azrael.py]
   379  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model   [nc/routes/azrael.py]
   343  GET              /api/backoff-watch                               api_backoff_watch   [nc/routes/beobachtung.py]
   230  POST             /api/backup/run                                  api_backup_run   [nc/routes/wartung.py]
   196  GET              /api/backup/status                               api_backup_status   [nc/routes/wartung.py]
   179  POST             /api/backup/system                               api_backup_system   [nc/routes/wartung.py]
   399  GET              /api/bandwidth/live                              api_bandwidth_live   [nc/routes/auskunft.py]
   532  GET              /api/beobachtung/dienste                         api_beobachtung_dienste   [nc/routes/beobachtung.py]
   525  GET              /api/beobachtung/lage                            api_beobachtung_lage   [nc/routes/beobachtung.py]
   547  POST             /api/beobachtung/steuern                         api_beobachtung_steuern   [nc/routes/beobachtung.py]
   376  GET              /api/bookmarks                                   api_bookmarks_list   [nc/routes/auskunft.py]
   198  GET              /api/brain                                       api_brain   [nc/routes/brain.py]
   131  GET              /api/brain/alarms                                api_brain_alarms   [nc/routes/brain.py]
   116  GET              /api/brain/creator                               api_brain_creator   [nc/routes/brain.py]
    93  GET              /api/brain/graph                                 api_brain_graph   [nc/routes/brain.py]
   158  GET              /api/brain/growth                                api_brain_growth   [nc/routes/brain.py]
    80  GET              /api/brain/health                                api_brain_health   [nc/routes/brain.py]
    81  POST             /api/chat/send                                   api_chat_send   [nc/routes/chat.py]
    53  GET              /api/chat/send_status                            api_chat_send_status   [nc/routes/chat.py]
   174  GET              /api/checks                                      api_checks   [nc/routes/auskunft.py]
    40  GET              /api/cohost                                      api_cohost   [nc/routes/cohost.py]
    52  POST             /api/cohost/config                               api_cohost_config   [nc/routes/cohost.py]
    52  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    87  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   122  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   443  GET              /api/community/stats                             api_community_stats   [nc/routes/auskunft.py]
   433  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   418  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   238  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
   195  POST             /api/cookies/fetch                               api_cookies_fetch   [nc/routes/settings.py]
    73  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    80  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   497  GET              /api/data/export                                 api_data_export   [nc/routes/auskunft.py]
   259  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   286  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   379  POST             /api/db/restore/apply                            api_db_restore_apply   [nc/routes/settings.py]
   323  GET              /api/db/restore/list                             api_db_restore_list   [nc/routes/settings.py]
   341  POST             /api/db/restore/prepare                          api_db_restore_prepare   [nc/routes/settings.py]
   246  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
   164  GET              /api/defense/attacks                             api_defense_attacks   [nc/routes/abwehr.py]
   125  GET              /api/defense/crowdsec                            api_defense_crowdsec   [nc/routes/abwehr.py]
   146  GET              /api/defense/fail2ban                            api_defense_fail2ban   [nc/routes/abwehr.py]
    91  GET              /api/defense/overview                            api_defense_overview   [nc/routes/abwehr.py]
   244  POST             /api/discord/announce                            api_discord_announce   [nc/routes/discord.py]
   170  GET              /api/discord/clips_week                          api_discord_clips_week   [nc/routes/discord.py]
   188  GET              /api/discord/community                           api_discord_community   [nc/routes/discord.py]
   160  GET              /api/discord/invite                              api_discord_invite   [nc/routes/discord.py]
    63  GET              /api/discord/overview                            api_discord_overview   [nc/routes/discord.py]
   136  POST             /api/discord/webhook_test                        api_discord_webhook_test   [nc/routes/discord.py]
    79  POST             /api/donations/add                               api_donations_add   [nc/routes/money.py]
   112  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   120  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    60  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   136  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
    56  GET              /api/einstellungen                               api_einstellungen   [nc/routes/einstellungen.py]
    68  POST             /api/einstellungen                               api_einstellungen_setzen   [nc/routes/einstellungen.py]
   102  POST             /api/einstellungen/uebernehmen                   api_einstellungen_uebernehmen   [nc/routes/einstellungen.py]
    86  POST             /api/einstellungen/zuruecksetzen                 api_einstellungen_zuruecksetzen   [nc/routes/einstellungen.py]
   194  GET              /api/evolution/changelog                         api_evolution_changelog   [nc/routes/evolution.py]
   179  GET              /api/evolution/history                           api_evolution_history   [nc/routes/evolution.py]
    90  GET              /api/evolution/learned                           api_evolution_learned   [nc/routes/evolution.py]
   112  GET              /api/evolution/proposals                         api_evolution_proposals   [nc/routes/evolution.py]
   133  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss   [nc/routes/evolution.py]
   150  POST             /api/evolution/proposals/bulk                    api_evolution_bulk   [nc/routes/evolution.py]
    80  POST             /api/evolution/run                               api_evolution_run   [nc/routes/evolution.py]
   209  GET              /api/evolution/snapshots                         api_evolution_snapshots   [nc/routes/evolution.py]
    44  GET              /api/evolution/status                            api_evolution_status   [nc/routes/evolution.py]
   204  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   224  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   251  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
   394  GET              /api/forecast/storage                            api_forecast_storage   [nc/routes/auskunft.py]
   297  GET              /api/freeai/status                               api_freeai_status   [nc/routes/auskunft.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
   414  GET              /api/heatmap/lives/<username>                    api_heatmap_lives   [nc/routes/auskunft.py]
   409  GET              /api/heatmap/recordings                          api_heatmap_recordings   [nc/routes/auskunft.py]
   485  GET              /api/highlights                                  api_highlights   [nc/routes/auskunft.py]
    64  GET              /api/i18n/katalog                                api_i18n_katalog   [nc/routes/i18n.py]
    53  GET              /api/i18n/sprachen                               api_i18n_sprachen   [nc/routes/i18n.py]
   307  GET              /api/i18n/uebersetzer.js                         api_i18n_js   [nc/routes/i18n.py]
    77  POST             /api/i18n/waehlen                                api_i18n_waehlen   [nc/routes/i18n.py]
   168  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    43  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   150  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   125  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   189  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    76  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    99  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   223  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
   222  GET              /api/kick/channel                                api_kick_channel   [nc/routes/kick.py]
   244  POST             /api/kick/channel                                api_kick_channel_set   [nc/routes/kick.py]
   103  GET              /api/kick/oauth/callback                         api_kick_oauth_callback   [nc/routes/kick.py]
   171  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect   [nc/routes/kick.py]
   149  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect   [nc/routes/kick.py]
    85  GET              /api/kick/oauth/start                            api_kick_oauth_start   [nc/routes/kick.py]
   128  GET              /api/kick/oauth/status                           api_kick_oauth_status   [nc/routes/kick.py]
   178  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck   [nc/routes/kick.py]
   119  POST             /api/kickmod/config                              api_kickmod_config   [nc/routes/kickmod.py]
   167  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords   [nc/routes/kickmod.py]
   184  GET              /api/kickmod/learned                             api_kickmod_learned   [nc/routes/kickmod.py]
   215  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear   [nc/routes/kickmod.py]
   191  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote   [nc/routes/kickmod.py]
   251  POST             /api/kickmod/say                                 api_kickmod_say   [nc/routes/kickmod.py]
   221  POST             /api/kickmod/start                               api_kickmod_start   [nc/routes/kickmod.py]
    82  GET              /api/kickmod/status                              api_kickmod_status   [nc/routes/kickmod.py]
   235  POST             /api/kickmod/stop                                api_kickmod_stop   [nc/routes/kickmod.py]
    66  GET              /api/lagebild                                    api_lagebild   [nc/routes/lagebild.py]
   428  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard   [nc/routes/auskunft.py]
    78  POST             /api/marketing/config                            api_marketing_config   [nc/routes/marketing.py]
   103  GET              /api/marketing/preview                           api_marketing_preview   [nc/routes/marketing.py]
   113  POST             /api/marketing/send-now                          api_marketing_send_now   [nc/routes/marketing.py]
    52  GET              /api/marketing/status                            api_marketing_status   [nc/routes/marketing.py]
    70  POST             /api/marketing/toggle                            api_marketing_toggle   [nc/routes/marketing.py]
   225  GET              /api/moderation/feed                             api_moderation_feed   [nc/routes/stats.py]
   100  POST             /api/news/config                                 api_news_config   [nc/routes/news.py]
    66  GET              /api/news/creators                               api_news_creators   [nc/routes/news.py]
    77  POST             /api/news/creators/generate                      api_news_creators_generate   [nc/routes/news.py]
   142  POST             /api/news/generate-now                           api_news_generate_now   [nc/routes/news.py]
   137  GET              /api/news/items                                  api_news_items   [nc/routes/news.py]
   128  GET              /api/news/preview                                api_news_preview   [nc/routes/news.py]
    53  GET              /api/news/status                                 api_news_status   [nc/routes/news.py]
    92  POST             /api/news/toggle                                 api_news_toggle   [nc/routes/news.py]
   257  GET              /api/ops/audit                                   api_ops_audit   [nc/routes/ops.py]
   324  GET              /api/ops/db-stats                                api_ops_db_stats   [nc/routes/ops.py]
   352  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown   [nc/routes/ops.py]
   203  GET              /api/ops/errors                                  api_ops_errors   [nc/routes/ops.py]
   270  GET              /api/ops/healthcheck                             api_ops_healthcheck   [nc/routes/ops.py]
   505  GET              /api/ops/log-tail                                api_ops_log_tail   [nc/routes/ops.py]
    80  GET              /api/ops/logtail                                 api_ops_logtail   [nc/routes/ops.py]
   168  GET              /api/ops/metrics                                 api_ops_metrics   [nc/routes/ops.py]
   151  GET              /api/ops/resource_history                        api_ops_resource_history   [nc/routes/ops.py]
   391  GET              /api/ops/version                                 api_ops_version   [nc/routes/ops.py]
   238  GET              /api/outcomes                                    api_outcomes   [nc/routes/auskunft.py]
   210  POST             /api/overlay/config                              api_overlay_config   [nc/routes/overlay.py]
   193  POST             /api/overlay/event                               api_overlay_event   [nc/routes/overlay.py]
    94  GET              /api/overlay/state                               api_overlay_state   [nc/routes/overlay.py]
   268  GET              /api/profile/<username>                          api_profile   [nc/routes/beobachtung.py]
   590  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk   [nc/routes/beobachtung.py]
   565  GET              /api/profile/snapshots/<username>                api_profile_snapshots   [nc/routes/beobachtung.py]
   308  GET              /api/public/stats                                api_public_stats   [nc/routes/auskunft.py]
   144  GET              /api/pulse                                       api_pulse   [nc/routes/auskunft.py]
   974  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
  1096  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
  1124  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
  1144  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   961  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
  1023  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
  1010  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   991  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   347  GET              /api/recording-attempts                          api_recording_attempts   [nc/routes/auskunft.py]
   636  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   631  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   679  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   562  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   889  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   653  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   616  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   589  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   863  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   733  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   822  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   728  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   661  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   441  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   906  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   529  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   784  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   939  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   924  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   485  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   723  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   709  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   692  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   749  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
  1287  GET              /api/recordings/session/<sid>                    api_recording_session   [nc/routes/recordings.py]
  1408  POST             /api/recordings/session/<sid>/join               api_recording_session_join   [nc/routes/recordings.py]
  1251  GET              /api/recordings/sessions                         api_recording_sessions   [nc/routes/recordings.py]
   842  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   738  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   490  POST             /api/restream/<int:rid>/delete                   api_restream_delete   [nc/routes/restream.py]
   468  POST             /api/restream/<int:rid>/edit                     api_restream_edit   [nc/routes/restream.py]
   509  POST             /api/restream/<int:rid>/start                    api_restream_start   [nc/routes/restream.py]
   526  POST             /api/restream/<int:rid>/stop                     api_restream_stop   [nc/routes/restream.py]
   578  GET              /api/restream/chatfeed                           api_restream_chatfeed   [nc/routes/restream.py]
   444  POST             /api/restream/create                             api_restream_create   [nc/routes/restream.py]
   265  GET              /api/restream/deck                               api_restream_deck   [nc/routes/restream.py]
   165  GET              /api/restream/health                             api_restream_health   [nc/routes/restream.py]
   600  POST             /api/restream/layout                             api_restream_layout   [nc/routes/restream.py]
   413  GET              /api/restream/list                               api_restream_list   [nc/routes/restream.py]
   134  POST             /api/restream/report                             api_restream_report   [nc/routes/restream.py]
   539  POST             /api/restream/start_all                          api_restream_start_all   [nc/routes/restream.py]
   565  POST             /api/restream/stop_all                           api_restream_stop_all   [nc/routes/restream.py]
   191  GET              /api/restream/testpush                           api_testpush_status   [nc/routes/restream.py]
   216  POST             /api/restream/testpush                           api_testpush_run   [nc/routes/restream.py]
   388  GET              /api/restream/verify                             api_restream_verify   [nc/routes/restream.py]
   148  GET              /api/retention/preview                           api_retention_preview   [nc/routes/wartung.py]
   160  POST             /api/retention/run                               api_retention_run   [nc/routes/wartung.py]
   474  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   464  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   499  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    65  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    86  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    52  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
   102  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   366  GET              /api/search                                      api_search   [nc/routes/auskunft.py]
    92  GET              /api/selftest                                    api_selftest   [nc/routes/selbsttest.py]
   456  GET              /api/shield/stats                                api_shield_stats   [nc/routes/auskunft.py]
   128  GET              /api/stats                                       api_stats   [nc/routes/stats.py]
   219  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern   [nc/routes/stats.py]
   214  GET              /api/stats/tiktok-status                         api_tiktok_status   [nc/routes/stats.py]
   274  GET              /api/stats/timeline                              api_stats_timeline   [nc/routes/stats.py]
   110  GET              /api/storage                                     api_storage   [nc/routes/wartung.py]
   116  POST             /api/storage/cleanup                             api_storage_cleanup   [nc/routes/wartung.py]
   578  GET              /api/stream/inspect/<username>                   api_stream_inspect   [nc/routes/beobachtung.py]
   397  GET              /api/stream/timeline                             api_stream_timeline   [nc/routes/beobachtung.py]
   427  GET              /api/stream/transcript                           api_stream_transcript   [nc/routes/beobachtung.py]
   126  GET              /api/streamer/compare                            api_streamer_compare   [nc/routes/streamer.py]
   273  POST             /api/streamer/delete/<username>                  api_streamer_delete   [nc/routes/streamer.py]
    88  GET              /api/streamer/detail                             api_streamer_detail   [nc/routes/streamer.py]
   298  GET              /api/streamer/digest/<username>                  api_streamer_digest   [nc/routes/streamer.py]
   230  GET              /api/streamer/dormant                            api_streamer_dormant   [nc/routes/streamer.py]
   254  GET              /api/streamer/exists/<username>                  api_streamer_exists   [nc/routes/streamer.py]
   185  GET              /api/streamer/journal/<username>                 api_streamer_journal   [nc/routes/streamer.py]
   150  GET/POST         /api/streamer/priority/<username>                api_streamer_priority   [nc/routes/streamer.py]
   210  GET              /api/streamer/watchlist                          api_streamer_watchlist   [nc/routes/streamer.py]
    56  GET              /api/streamers/wall                              api_streamers_wall   [nc/routes/streamer.py]
   219  GET              /api/summary/preview                             api_summary_preview   [nc/routes/auskunft.py]
    74  GET              /api/system                                      api_system   [nc/routes/systemlage.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
   178  GET              /api/system/check_timing                         api_check_timing   [nc/routes/systemlage.py]
   118  GET              /api/system/config_drift                         api_config_drift   [nc/routes/systemlage.py]
   141  GET              /api/system/config_snapshot                      api_system_config_snapshot   [nc/routes/systemlage.py]
   238  GET              /api/system/preflight                            api_system_preflight   [nc/routes/systemlage.py]
   105  GET              /api/system/preflight_history                    api_system_preflight_history   [nc/routes/systemlage.py]
   375  GET              /api/system/resilience                           api_system_resilience   [nc/routes/systemlage.py]
   389  GET              /api/tags                                        api_tags_list   [nc/routes/auskunft.py]
   189  GET              /api/top                                         api_top   [nc/routes/auskunft.py]
   239  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   460  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   489  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   409  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   422  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   518  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   395  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   270  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   315  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   339  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   326  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   166  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   284  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   136  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   376  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   431  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
   265  GET              /api/trend-7d                                    api_trend_7d   [nc/routes/auskunft.py]
   121  POST             /api/tunnel/set                                  api_tunnel_set   [nc/routes/ops.py]
   100  GET              /api/tunnel/status                               api_tunnel_status   [nc/routes/ops.py]
   132  POST             /api/tunnel/test                                 api_tunnel_test   [nc/routes/ops.py]
   113  POST             /api/tunnel/toggle                               api_tunnel_toggle   [nc/routes/ops.py]
   125  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback   [nc/routes/twitch.py]
    77  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect   [nc/routes/twitch.py]
   101  GET              /api/twitch/oauth/start                          api_twitch_oauth_start   [nc/routes/twitch.py]
    55  GET              /api/twitch/oauth/status                         api_twitch_oauth_status   [nc/routes/twitch.py]
   453  GET              /api/update/backups                              api_update_backups   [nc/routes/ops.py]
   419  GET              /api/update/check                                api_update_check   [nc/routes/ops.py]
   478  POST             /api/update/restart                              api_update_restart   [nc/routes/ops.py]
   458  POST             /api/update/rollback                             api_update_rollback   [nc/routes/ops.py]
   441  POST             /api/update/start                                api_update_start   [nc/routes/ops.py]
   434  GET              /api/update/status                               api_update_status   [nc/routes/ops.py]
   251  GET              /api/userstats                                   api_userstats   [nc/routes/auskunft.py]
   317  GET              /api/version                                     api_version   [nc/routes/auskunft.py]
    52  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    92  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   123  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
   107  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
   131  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback   [nc/routes/youtube.py]
   152  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget   [nc/routes/youtube.py]
   164  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout   [nc/routes/youtube.py]
    89  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect   [nc/routes/youtube.py]
   113  GET              /api/youtube/oauth/start                         api_youtube_oauth_start   [nc/routes/youtube.py]
    67  GET              /api/youtube/oauth/status                        api_youtube_oauth_status   [nc/routes/youtube.py]
   199  GET              /api/youtube/sendrate                            api_youtube_sendrate   [nc/routes/youtube.py]
    73  GET              /fonts/<name>                                    schrift   [nc/routes/schriften.py]
    66  GET              /fonts/schriften.css                             schriften_css   [nc/routes/schriften.py]
   469  GET              /metrics                                         api_prometheus_metrics   [nc/routes/beobachtung.py]
```

## Discord-Slash-Commands in discordbot.py (66)

```
  2183  /about                  Ueber diesen Bot
   902  /ai                     
  2183  /aireset                KI-Kontext zuruecksetzen
  1314  /ask                    
  1003  /assign_role            
  1053  /ban                    
  2138  /botstats               
  2183  /brain                  Brain-Lage: Regeln, Agenten, Empfehlungen
  2183  /bulkadd                Mehrere User auf einmal tracken · a b c
  2183  /cleanup                Alte Aufnahmen aufraeumen
  1569  /clearwarns             
  2102  /clip                   
  2087  /clipoftheweek          
  1440  /clips                  
  2183  /cookies                Cookie-Status — mit 'holen' selbst beziehen · [holen]
   958  /create_category        
   929  /create_channel         
   993  /create_group           
   968  /create_role            
   944  /create_voice           
  1192  /daily                  
  2183  /diag                   Vollstaendige Diagnose
  2183  /einnahmen              Einnahmen und Spenden
  1343  /event                  
  1385  /events                 
  1479  /follow                 
  1468  /help                   
  1043  /kick                   
  1167  /leaderboard            
  2183  /live                   Live-Status sofort pruefen · @user
  1427  /livenow                
  2183  /logs                   Letzte Fehler aus dem Log
  2183  /pause                  Tracking pausieren · @user
  1455  /post_test              
  1275  /profile                
  1075  /purge                  
  2183  /quelle                 Stream-Quellen eines Live-Nutzers messen (alle Wege, ffprobe
  2183  /quota                  Speicher-Quota
  1154  /rank                   
  1415  /recstatus              
  1013  /remove_role            
  2183  /report                 Azrael-Sentinel-Wochenreport
   915  /restream_status        
  2183  /resume                 Tracking fortsetzen · @user
  1023  /set_channel_perms      
  1118  /setup_community        
  1135  /setup_targets          
  1511  /stats                  
   874  /status                 
  2183  /stoprec                Laufende Aufnahme sauber beenden · @user
  1607  /streaminfo             
  2183  /summary                Tageszusammenfassung
  2183  /sysres                 System-Ressourcen
  2183  /teststream             Recorder-Selbsttest · @user
  2183  /tiktok                 Profil-Analyse eines TikTok-Accounts · ‹name›
  1063  /timeout                
  1579  /topstreamers           
  2183  /topusers               Top-Streamer nach Aufnahmen
   804  /track                  
  2183  /track_exact            Exakten Usernamen tracken (ohne Korrektur) · ‹name›
   887  /tracklist              
  1493  /unfollow               
  2183  /unpause                Auto-pausierte Quelle wieder aktivieren · @user
   836  /untrack                
  1532  /warn                   
  1555  /warnings               
```

## Discord-Events in discordbot.py (4)

```
  2341  on_member_join
  2303  on_message
  2204  on_raw_reaction_add
  2376  on_ready
```

## Top-Level-Symbole in telegramversand.py (2 Funktionen)

```
    58-73     konfiguriere
    76-476    split_and_send_video
```

## Top-Level-Symbole in discordbot.py (51 Funktionen)

```
   490-495    _alle_getrackten
  1684-1735   _award_xp
  1906-1935   _clip_week_leader
  1959-1973   _clipoftheweek_loop
  2493-2555   _community_events_loop
  1641-1663   _dc_client
  1666-1675   _dc_offen
  2595-2630   _disc_automod_check
   405-410    _disc_sprache_setzen
  1738-1786   _discord_ai_automod
   625-664    _discord_automod
  1789-1809   _discord_azrael_reply
  1976-2452   _discord_run_once
   240-298    _discord_start
   301-355    _ensure_discord_invite
  2458-2490   _ensure_error_channel
   426-439    _ensure_rank_roles
   767-781    _ensure_team_roles
  2558-2588   _error_channel_loop
   674-678    _guard
   594-622    _handle_voice_ai
   413-423    _is_admin
  1854-1865   _liveboard_loop
   681-699    _on_level_up
   590-591    _par_chat_id
  1938-1956   _post_clip_of_week
  1868-1886   _post_weekly_digest
   442-468    _provision_base_channels
   471-487    _provision_user_channels
  1407-1500   _reg_betrieb
  1089-1181   _reg_community_setup
  1184-1264   _reg_daily_profil
  1307-1404   _reg_frage_events
   861-917    _reg_info
  1035-1086   _reg_moderation
  1267-1304   _reg_profil
   984-1032   _reg_rollen
   920-981    _reg_server
  1503-1590   _reg_streamer
  1593-1638   _reg_system
   795-858    _reg_tracking
   734-764    _run_tg_handler
   577-587    _tracked_usernames
   157-219    _uebernehmen
  1818-1851   _update_liveboard
  1889-1903   _weekly_digest_loop
   498-503    _ziel_guild
   506-548    _ziele_abgleichen
   557-574    _ziele_sync_loop
   551-554    _ziele_takt_min
   222-225    starte
```

## Top-Level-Symbole in bot.py (563 Funktionen, 3 Klassen)

```
 25765-25787  _abbruch_datenbank_unlesbar
  2667-2668   _abo_key
  2688-2706   _abo_probe_dump
 25883-25899  _abschied_wachen
 25902-25920  _abschluss
 16297-16304  _ad_allowlist
 17299-17305  _agent_for
 17308-17324  _ai_telemetry
 17821-17839  _alert
 21672-21722  _alert_monitor_loop
 18500-18557  _alte_beilagen_einsammeln
 22104-22166  _announce_loop
  3563-3573   _anthropic_key
  3580-3582   _anthropic_model
  9923-9926   _arg_int
  2659-2664   _as_dict
 25456-25465  _async_exc_handler
 18002-18024  _audio_tap_cmd
 18954-19013  _audio_tap_melden
 18038-18062  _audio_tap_sammler
  9267-9304   _aufnahme_beim_stopp_sichern
 18442-18463  _aufnahme_chat_ausklang
 18426-18439  _aufnahme_chat_beginnen
 18723-18773  _aufnahme_chat_einarbeiten
 18421-18423  _aufnahme_chat_modus
 18560-18606  _aufnahme_chat_nachtrag
 18466-18497  _aufnahme_chat_vormerken
 24705-24707  _aufnahme_deckel
 18609-18628  _aufnahme_fertigmachen
  9307-9325   _aufnahme_platz_frei
 25847-25867  _aufnahmen_abschliessen
 25790-25844  _aufraeumen
 10122-10191  _auth_cookie
 10080-10118  _auth_guard
  1908-1913   _auto_on
 19640-19658  _auto_restream_loop
 13927-13969  _avatar_frames_laden
 23238-23253  _azrael_broadcast_reply
 23138-23160  _azrael_chat_reply
 23110-23135  _azrael_chat_should_reply
 23166-23168  _azrael_gate_cfg
 17329-17343  _azrael_live_state
 20690-20704  _azrael_overlay_state
 17703-17757  _azrael_proactive_loop
 17147-17203  _azrael_reaction_to_chats
 23171-23178  _azrael_reply_all_chats
 23097-23107  _azrael_self_names
 23206-23235  _azrael_send_to
 13888-13924  _azrael_spricht
 14231-14244  _azrael_stimme_stumm
 17349-17370  _azrael_system
 21806-21809  _backup_active
 21887-21900  _backup_loop
 24794-24798  _betrieb
 25529-25538  _brain_crowdsec_snap
 25692-25695  _brain_db_health
 21593-21602  _brain_growth_loop
 10517-10544  _brain_growth_snapshot
  2592-2612   _brain_hint_delay
 25601-25636  _brain_moderation_snap
  6509-6537   _brain_notify
 25698-25720  _brain_recording_snap
 25541-25598  _brain_restream_health
 25723-25736  _brain_tiktok_status_snap
 11816-11833  _browser_push
  6549-6636   _build_daily_summary
 14278-14282  _build_restream_cmd
  5262-5289   _can_stop_tracking
  2021-2043   _capture_set_cookies
 12501-12504  _cfg_get
 12507-12509  _cfg_set
 20412-20447  _channel_set_all
 13084-13087  _chat_connected
 13090-13106  _chat_disconnected
  8896-8907   _chat_is_forum
 18390-18415  _chat_listener_abbauen
 13126-13128  _chat_sanitize
 13069-13081  _chat_stat
 13109-13112  _chat_stats_snapshot
  3881-3893   _check_ai_models_sync
 10799-10842  _classify_pool_anonymity
 10845-10862  _classify_pool_anonymity_bg
   899-921    _claude_chat_sync_metered
  9955-9961   _client_ip
 22737-22751  _clip_chat_ass
 22250-22284  _clip_prune
 22287-22297  _clip_recfile_for
 22660-22725  _clip_schneiden
 22754-22760  _clip_should_velocity
 22339-22421  _clip_to_discord
 18694-18699  _clips_abwarten
  3767-3776   _close_ai_session
 23284-23299  _cohost_broadcast
 23269-23270  _cohost_cfg
 23325-23337  _cohost_fire_highlight
 23273-23281  _cohost_gate
 23302-23322  _cohost_highlight
 10447-10449  _conv_messages
  6908-6969   _cookie_alarm_loop
  2111-2112   _cookie_autofetch_info
  2095-2099   _cookie_autorefresh_info
 25163-25185  _cookie_bezug_loop
 25188-25213  _cookie_bezug_runde
  1998-2002   _cookie_header
  9964-9969   _cookie_sicher
  2124-2138   _cookies_selbst_holen
  4097-4099   _create_index_safe
 21136-21250  _crowdsec_status
 21082-21133  _crowdsec_via_lapi
 20986-21004  _cscli_bin
 21013-21026  _cscli_path
  6798-6823   _daily_summary_loop
 21044-21061  _darf_journal_lesen
  3092-3117   _darf_ytdlp_nachschlagen
 11997-12018  _dashboard_adresse
 22728-22734  _datei_weg
 21646-21669  _db_maintenance_loop
  6767-6795   _db_vacuum_loop
 16320-16344  _detect_foreign_ad
  1588-1599   _diag_path_owner
 17608-17653  _director_finalize
 18943-18950  _director_for
 17557-17605  _director_mark
 22573-22576  _disc_state_get
 22579-22586  _disc_state_set
 21574-21583  _discord_bot_starten
 21537-21548  _discord_einladung_merken
 21586-21590  _discord_invite
 21551-21571  _discord_kontext
 22534-22570  _discord_live_thread
 17760-17772  _discord_notify
 21509-21534  _discord_ops_alert
 22432-22530  _discord_post_user
 22169-22175  _discord_stop
  6826-6903   _disk_alarm_loop
 25088-25137  _disk_autoclean
 25311-25324  _disk_guard_loop
 13866-13873  _drossel_hoeher
 13862-13863  _drossel_stufe
 13876-13884  _drossel_zuruecksetzen
 12174-12176  _dump_all_threads
 24801-24815  _einstellungen_startzeile
 10725-10788  _enrich_proxies_with_geo
  2167-2228   _ensure_cookie_file_netscape
  8955-8958   _ensure_notify_topic
 10969-11006  _ensure_proxy_ready
  8909-8936   _ensure_topic
   741-743    _env_int
   746-748    _env_int_range
 17805-17818  _event_webhook
 12852-12865  _evolution_loop
  5951-5985   _extract_file_payload
  2300-2302   _extract_urls_from_streamurl_node
 21029-21036  _f2b_sudo_hint
 25923-25986  _fatal_vom_botteil
 24710-24725  _fd_grenze_anheben
  4726-4736   _fehler_text
 10626-10644  _fetch_proxy_list
 18359-18387  _fetch_tiktok_room_id
   824-827    _ff_cmd
 18707-18720  _ffprobe_masse
 13695-13700  _find_chromium
  3483-3485   _find_external_recorder
  2305-2307   _find_stream_urls
 12552-12577  _fire_webhooks
  7735-7744   _fork_safe
   932-945    _freeai_chat_sync_metered
 21075-21079  _geo_lookup_ips
  3755-3764   _get_ai_session
  7568-7608   _get_live_info
  2943-2950   _get_resolve_semaphore
  8153-8549   _handle_single_tracking
 24910-24912  _hb
 24915-24932  _hb_while
 13140-13142  _highlight_cfg
 13145-13174  _highlight_observe
 13703-13721  _htmlov_screenshot_cmd
 18064-18074  _httpx_proxy
 12585-12597  _in_quiet_hours
 25751-25762  _init_db_oder_abbruch
 26570-26601  _install_fast_eventloop
  9818-9872   _install_fast_json
 12179-12195  _install_faulthandler
 19691-19700  _intel_ensure_schema
 19743-19778  _intel_index_loop
 19712-19727  _intel_index_one
 19703-19709  _intel_semantic
  5251-5260   _is_authorized
  8039-8060   _is_dead
  2290-2292   _is_hevc
 21064-21066  _is_private_ip
  1807-1814   _is_process_running
  6539-6546   _is_quiet_hours
  1381-1390   _is_upload_window
  4591-4606   _iso
  9972-9978   _ist_lokal
  9907-9920   _json_error_handler
  6761-6762   _kick_broadcaster_id
  7939-7946   _kick_cluster_gefunden
  7895-7936   _kick_cluster_weiter
  6673-6715   _kick_follower_count
  6657-6660   _kick_slug
 11629-11636  _kick_user_token
  7867-7892   _kick_ws_pause
 25739-25748  _kickmod_boot
  4181-4184   _kind_from_filename
 12614-12616  _latest_popularity
  1744-1753   _laufstand
 25271-25308  _laufstand_loop
 24834-24872  _leistung_erheben
 19349-19398  _live_react_loop
 19016-19338  _live_react_worker
  3333-3445   _live_status_aufloesen
 17206-17217  _live_transcript_push
 19340-19347  _live_users
 17656-17700  _living_title_loop
 21812-21884  _local_backup_scan
  9889-9903   _log_5xx
 24875-24907  _log_schleuse_pruefen
   814-821    _log_sicher
 14290-14302  _looks_like_codec_err
 14285-14287  _looks_like_source_expired
  7785-7815   _loop_fehler
 12199-12208  _loop_heartbeat
 24616-24649  _loop_lag_monitor
 24663-24683  _loop_stockung_melden
 24686-24696  _loop_takt_starten
 12211-12284  _loop_watchdog_thread
 17083-17100  _loyalty_add
 17074-17080  _loyalty_get
 17103-17111  _loyalty_top
 12724-12726  _manual_donations_total
  4933-4952   _manual_status
  8062-8063   _mark_dead
 11245-11261  _marketing_loop
 23185-23203  _maybe_handle_command
 25410-25434  _maybe_hype_clip
 22219-22247  _meme_klassifizieren
 18631-18691  _meme_zusammenschnitt
  4084-4089   _migrate_columns
 23464-23475  _mod_is_exempt
 23478-23483  _mod_warn_first
 23486-23489  _mod_warn_text
 12909-12928  _modlog
 12892-12906  _modlog_schreiben
  1077-1079   _multistream_targets
  3120-3156   _nachschlag_ytdlp
  7747-7748   _nc_create_subprocess_exec
  7751-7752   _nc_create_subprocess_shell
 11566-11583  _news_loop
 12951-12953  _normalize_ingest
  2523-2540   _note_check_duration
  8949-8952   _notify_topic_name
  2713-2719   _offline_ergebnis
  3159-3179   _ohne_url_melden
 17232-17240  _oracle_memories
 17506-17540  _oracle_memorize
 17243-17256  _oracle_persona
 17225-17229  _oracle_recent_text
 13329-13330  _ov_atomic_write
 13320-13322  _ov_bar
 16223-16235  _ov_clip_text
 13325-13326  _ov_oneline
 20741-20770  _overlay_push
 13649-13692  _overlay_render_size
 13020-13024  _overlay_session_reset
 20706-20708  _overlay_src_ok
 16307-16317  _own_invites
 13644-13646  _parse_size
 21258-21338  _parse_ssh_attacks
  7170-7203   _pause_resume_cmd
  2049-2093   _persist_refreshed_cookies
  1952-1984   _pick_checked_pull_proxy
 10009-10022  _pin_auth_value
 10069-10070  _pin_clear_fail
 10049-10052  _pin_locked
 10055-10066  _pin_note_fail
 10025-10046  _pin_ok
 20548-20573  _piper_pick_model
 20633-20684  _piper_say
 12514-12549  _post_json_threaded
 13623-13641  _probe_video_size
  1835-1852   _proc_is_recorder
 10938-10966  _proxy_pool_refresh_loop
  1918-1949   _proxy_report_recording
  8647-8685   _pruefstand_melden
 24745-24756  _pruefung_verworfen
 12164-12166  _prune_stall_dumps
 11315-11485  _public_stats
  2115-2121   _pull_proxy_still
 17776-17802  _push_notify
 10238-10240  _pwa_dir
 10695-10710  _quick_validate_proxy
 12580-12582  _quiet_hours_config
 10203-10236  _rate_guard
 17044-17050  _react_warn
  7655-7694   _reap_proc
  9197-9264   _rec_auto_abschalten
  9144-9194   _rec_frueh_getrennt
  9013-9089   _rec_kategorie_melden
  9092-9141   _rec_totstreak_fortschreiben
  2563-2585   _record_check_outcome
   809-811    _redact_stream_urls
 10865-10935  _refresh_proxy_pool
  2340-2431   _resolve_via_html
  2722-2920   _resolve_via_webcast_api_v2
  2983-3068   _resolve_via_ytdlp
 22794-22923  _resolve_youtube_ingest
  2316-2337   _resolver_stumm
 13003-13014  _restream_active_sources
 13972-14096  _restream_avatar_feeder_start
 14099-14108  _restream_avatar_feeder_stop
 18776-18907  _restream_chat_guardian
 13177-13249  _restream_chat_push
 13306-13315  _restream_chat_push_async
 25639-25689  _restream_durchreicher
 13724-13833  _restream_html_overlay_start
 13836-13849  _restream_html_overlay_stop
 12962-12985  _restream_overlay_files
 19402-19434  _restream_platform_state
 19602-19637  _restream_resume_after_restart
 13280-13303  _restream_status_schreiben
 14156-14228  _restream_tts_enqueue_wav
 13585-13617  _restream_tts_feeder
 13582-13583  _restream_tts_fifo_path
 14111-14138  _restream_tts_start
 14140-14154  _restream_tts_stop
 19440-19599  _restream_verify_loop
 21777-21789  _retention_loop
 21771-21774  _retention_scan
  2670-2672   _room_is_abo
  5989-6106   _run_ai_call
 12307-12320  _run_async_from_flask
 21069-21072  _run_priv
 26558-26566  _run_selfcheck_and_exit
 21792-21803  _s3_client
  8089-8140   _safe_send
  4859-4875   _sample_net_throughput
  2615-2645   _schedule_next_check
 21725-21768  _scheduler_loop
  4092-4094   _schema_pk
 12324-12329  _scraper_session
 23492-23531  _screen_full
 11680-11717  _sec_headers
  2295-2297   _select_stream_from_data_section
 26278-26555  _selfcheck
  8961-8995   _send_live_notice
  1404-1408   _should_defer_upload
 22300-22336  _shrink_for_discord
 10243-10255  _sicheres_ziel
 21605-21643  _sicherheits_erinnerung_loop
 25331-25348  _sign_health_check
 25351-25370  _sign_health_loop
  4609-4634   _sitzung_bestimmen
  7764-7775   _spawn
 26983-27013  _spawn_from_flask
 24759-24765  _speicher_maps
 24768-24783  _speicher_pflegen
 18076-18356  _start_chat_listener
 24728-24742  _start_gesperrt
 12287-12304  _start_loop_watchdog
 11512-11561  _stats_loop
 11491-11494  _stats_output_path
 11497-11509  _stats_write
 20585-20599  _stimme_saubern
 20606-20630  _stimme_schon_gesagt
  8628-8644   _storage_cleanup_loop
 25390-25397  _story_for
  3508-3514   _stream_url_expiry
  3516-3521   _stream_url_ttl
 16270-16277  _streamer_persona_get
 21909-22061  _system_backup
 22070-22100  _system_backup_loop
 12124-12142  _task_auf_bot_schleife
 24305-24321  _telegram_befehlsmenue
  7818-7864   _telegram_polling_fehler
 10647-10686  _test_proxy
 11193-11209  _testpush_resolve_live
 18702-18704  _text_schreiben
  8065-8086   _tg_sprache_setzen
  8868-8878   _tg_topics_load_into_mem
  8865-8866   _tg_topics_path
  8880-8887   _tg_topics_save
  9981-9991   _token_ok
  8890-8894   _topic_forget
 12600-12611  _tracking_max_duration
  4389-4403   _tracking_remove_cleanup
  4420-4432   _tracking_resume_cleanup
  1646-1669   _try_attach_file_handler
 20575-20583  _tts_cleanup
 11169-11173  _tunnel_effective
 25140-25160  _tunnel_lage
 25216-25268  _tunnel_wacht_loop
 20071-20124  _twitch_channel_status
 23534-23679  _twitch_chat_loop
 22592-22605  _twitch_clip_versuchen
 23348-23451  _twitch_eventsub_loop
  1427-1440   _upload_queue_add
  1451-1453   _upload_queue_count
  1410-1419   _upload_queue_load
  1400-1402   _upload_queue_path
  1442-1449   _upload_queue_remove
  1421-1425   _upload_queue_save
  1455-1496   _upload_window_loop
  7628-7635   _uptime_s
 12939-12948  _url_host
  3182-3281   _url_nachschlag
   892-896    _usage_record_claude
 25504-25526  _v37_pause_source
 25468-25478  _v37_restream_restart
 25481-25501  _v37_unpause_source
  7988-8032   _verbindung_verloren
  6718-6749   _viewer_sample_loop
 10073-10076  _wants_html
  7638-7652   _warn_empty_env
 24953-25074  _watchdog_loop
 23069-23077  _wchat_thank_ok
 17844-17874  _whisper_get_model
  7725-7732   _whisper_native_section
 17031-17037  _whisper_pool
 17968-18000  _whisper_segments
 17876-17892  _whisper_stumm
 17895-17965  _whisper_transcribe
 13377-13539  _write_restream_overlay
 13339-13374  _write_restream_overlay_async
 23703-23799  _youtube_api_chat_loop
 20127-20230  _youtube_api_status
 20233-20300  _youtube_channel_status
 23802-23963  _youtube_chat_loop
 22608-22633  _youtube_clip_versuchen
 22929-22942  _youtube_restream_autoconfig
 22945-22969  _youtube_restream_autoconfig_inner
 23036-23064  _youtube_send
 20368-20409  _youtube_set_channel
 22972-23006  _yt_access_token
 23009-23024  _yt_live_chat_id
 23032-23033  _yt_sendrate_cfg
 23682-23697  _yt_timeout
  2967-2968   _ytdlp_detect_available
  2970-2981   _ytdlp_note_result
 12169-12171  _zombie_child_count
 24818-24831  _zustand_kennzahlen
  7504-7528   about
  4300-4304   add_ai_log_entry
  4217-4220   add_archive_entry
  4897-4899   add_archive_rule
  4637-4708   add_recording
  4364-4381   add_tracking
  6109-6142   ai
  3907-3988   ai_chat
  4022-4032   ai_history_append
  4034-4039   ai_history_clear
  4011-4020   ai_history_load
  3996-4009   ai_rate_limit_check
  6171-6179   aireset
 17373-17392  azrael_chat
 23968-24090  brain_cmd
  3524-3529   build_recording_cmd
  4384-4387   bulk_add_trackings
  6972-7031   bulkadd
  8688-8848   check_all_trackings
  4436-4448   claim_live_transition
 16347-16963  class KickModerator
 14305-16110  class RestreamManager
  7949-7985   class _KickClusterSuche
 11052-11094  classify_proxy_anonymity
  6217-6415   cleanup
  5187-5193   cleanup_old_recordings
  4582-4589   clear_recording
 22636-22657  clip_moment
  4849-4852   compute_storage_forecast
  7094-7167   cookies_cmd
  4355-4361   count_trackings_for_chat
  4287-4298   decide_preferred_recorder
  4227-4230   delete_archive_entry
  4901-4903   delete_archive_rule
  5646-5793   diag
 24202-24263  einnahmen_cmd
  4843-4846   find_recordings_by_fingerprint
  4248-4264   finish_recording_attempt
  4408-4410   get_all_active_trackings
  4315-4317   get_all_checks
  4710-4713   get_all_recordings
  4792-4794   get_all_tags_with_counts
  4820-4823   get_annotations_for_recording
  4222-4225   get_archive_entry
  4813-4816   get_bookmarked_recordings
  2155-2160   get_cookie_health
  4780-4786   get_event_log
  4271-4285   get_last_recording_attempt
  3284-3326   get_live_status
  5126-5129   get_manual_recordings
  4828-4831   get_or_compute_inspect_sync
  5228-5231   get_outcome_breakdown
  4799-4802   get_priority_poll_interval
  4266-4269   get_recent_recording_attempts
  4715-4718   get_recording_by_id
  4806-4809   get_recording_note
  3695-3724   get_redis
  4344-4347   get_stats
  5181-5185   get_storage_stats
  4921-4923   get_tiktok_status_distribution
  4450-4459   get_tracking_state
  4405-4406   get_trackings_for_group
  5142-5145   get_trash_recordings
  9328-9797   handle_recording_finished
 24297-24302  hilfe_cmd
  4107-4172   init_db
  4893-4895   list_archive_rules
  5431-5469   live
  8143-8151   live_check_worker
  3779-3818   llm_chat
  3841-3871   llm_chat_sync
  3826-3838   llm_list_models
  4739-4772   log_event
  1769-1802   log_recording_failure
  7317-7366   logs_cmd
 25989-26268  main
  6145-6168   on_ai_media
  7443-7469   on_ai_reply
  7472-7501   on_azrael_mention
  7533-7563   on_callback
 17398-17503  oracle_handle
  7206-7209   pause_tracking
  5241-5246   profile_keyboard
  5384-5428   quelle
  7268-7314   quota
  8551-8625   reaper_loop
  4917-4919   record_tiktok_status
  6184-6214   recstatus
  3726-3734   redis_get_json
  3737-3743   redis_set_json
 24324-24334  report_cmd
 11097-11099  report_proxy_result
  2434-2476   resolve_tiktok_live_stream
  5137-5140   restore_recording
  7212-7215   resume_tracking
  4906-4911   run_archive_rules
 24337-24596  run_bot
 12021-12115  run_flask
  4881-4884   sample_bandwidth_for_active
  4307-4313   save_tiktok_check
  4574-4580   set_recording_file
  4413-4417   set_tracking_paused
  5132-5135   soft_delete_recording
  9001-9011   split_and_send_video
  5294-5336   start
  4232-4246   start_recording_attempt
  6418-6456   stats
  5071-5124   stop_manual_recording
  7218-7265   stoprec
  6642-6650   summary_cmd
  7369-7440   sysres
  5795-5939   teststream
  5338-5379   tiktok
  7034-7091   topusers
  5506-5563   track
  5471-5503   track_exact
  5577-5644   tracklist
  4955-5069   trigger_manual_recording
  4535-4572   try_acquire_recording_lock
  5148-5150   universal_search
 24266-24294  unpause_cmd
  5565-5575   untrack
 24093-24199  update_cmd
  4838-4841   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, class BestandUnbekannt, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, finde_ohne_eintrag, get_archive_entries_paged, get_archive_entry, run_archive_file_check, uebernehmen
archivename.py         open_unique
archiverules.py        add_archive_rule, delete_archive_rule, list_archive_rules, run_archive_rules
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
audiocue.py            config, configure
audiotap.py            diagnose, melden, warum_kein_tap
aufnahmechat.py        ass, ausschnitt, beenden, beginnen, clip_beginnt, clip_fertig, clip_merken, clips_nehmen, clips_offen, concat_liste, einbrennen_cmd, laeuft, modus, notieren, untertitel_cmd, zusammenschnitt_cmd
aufnahmefolge.py       aufnahme_geglueckt, daten_geflossen, melden_erlaubt, nach_403, nach_frueher_trennung, nach_totem_versuch, sitzung_zuende, sperre_rest, stall_grenze
aufnahmekategorie.py   kategorisiere
aufnahmesitzung.py     abdeckung, angleich_cmd, braucht_angleich, concat_cmd, concat_liste, gehoert_dazu, luecken, probe_cmd, sekunden, sitzung_id, tonformat, zieldatei
auslieferung.py        schreibe, stand, text
avatarloop.py          blinzeln, ruhe_seit, schleife, zustand
azraelstate.py         configure, flag, haken, personas_load, personas_path, personas_save
backupcfg.py           aktiv, fehlgrund, lokal, lokal_dir, recordings_retain_days, retention_days, s3, s3_bucket, s3_endpoint, s3_konfiguriert, s3_region, s3_zugang, sys_backup, sys_hour, sys_keep, sys_max_file_mb
badwords.py            banned_path, configure, fetch_ldnoobw_de, learned_path, load_banned, load_learned, save_banned, save_learned
bandbreite.py          messen
befehle.py             beschreibung, discord_nativ, discord_ueber_tg, fuer, hilfe_text, pruefen, telegram_handler
beobachtungsdienst.py  fuer_deck, grafana_jetzt, grafana_lage, grafana_unit, grund_text, installiert, prometheus_jetzt, prometheus_lage, selbstheilung_erlaubt, steuern
beobachtungslage.py    grafana, lage, prometheus
betriebslage.py        abschiedswache, bereit, bewerten, haengende_threads, sichern_beim_stopp
binresolve.py          resolve
botctx.py              class BotKontext
brainstate.py          history_for, record, stall, stream_recent
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat, restream_active, yt_sendrate_cfg
chatfolge.py           entscheide
chatnachtrag.py        beilage_lesen, beilage_zu, eingearbeitet, ensure_schema, erledigt, fehlversuch, ist_beilage, lesen, offene, stempel, unveraendert, vormerken
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, fehlertext, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
clientip.py            echte_ip, ist_https, ist_lokal
cohost.py              config, decide, default_config, new_state, prompt_seed, snapshot
community.py           anzeigename, configure, darf_pingen, highlight_post, highlight_share_enabled, live_ping, live_ping_enabled, note_chatter, returning_enabled, rollen_id, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookiebezug.py         anstossen, configure, faellig, gast_hilft, holen, info, intervall_s, naechster_lauf
cookieholen.py         aktualisiere, aus_browser, configure, hole_gastcookies, schreibe, zusammenfuehren
cookies.py             configure, gesundheit, lade_jar, load_dict
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, erwartete_namen, fehlende_namen, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dashauth.py            erlaubt_offen, geschuetzt, host, lage, nur_lokal, offen_im_netz, zurueckgefallen
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbgesundheit.py        messen
dbrestore.py           archive, dump_aus_archiv, einsetzen, einspielen, vorbereiten
dbwrap.py              class DatenbankUnlesbar, configure_db, datei_diagnose, db_async, db_conn, get_pool, set_pool
ddlsafe.py             ddl, ist_schon_da
defensecfg.py          bouncer_gesetzt, bouncer_key, geo_fehler, geo_fehler_setzen, lapi_host, lapi_port, lapi_url, server_lat, server_lon
director.py            class LiveDirector, configure
discordlimits.py       aktuell_label, aktuell_mb, configure, describe, effective_upload_mb, gate_mb, guild_filesize_bytes, guild_limit_mb
discordrang.py         rang_fuer_level, slug, xp_fuer_level, xp_zu_level
discordstate.py        invite, state_get
discordziele.py        eigene_kanaele, kategorie, loeschbar, plan
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur, unknown_count
donationsdb.py         manual_rows, manual_total, parse_eur
durchreicher.py        adresse, ist, main, nutzer_aus, werkzeug, zieher_cmd, zieher_umgebung, zubringer_cmd
einstellungen.py       class Abgelehnt, db_werte, geheim, gueltiger_name, in_umgebung_laden, katalog, pruefen, schutzgrund, setzen, startbericht, uebernehmen, uebersicht, zuruecksetzen
envdatei.py            class EnvdateiFehler, lesen, main, setzen, wert_lesen, wert_schreiben
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventlog.py            leeren, schreibe, stand
eventquery.py          build_query
evolution.py           analyze, build_dir, conf, configure, cycle, engineering_note, next_version, write_build
fehlertext.py          nach_aussen, saeubern
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      anzeige_groesse, avatar_kette, chat_umbruch_w, chat_zeilen, drawtext_chain, studio_chain, studio_masse
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, dienstmeldung, katalog_kennt, last_errors, list_models_sync, stream_haeppchen, stream_rest
gegendruck.py          abgewiesen, deckel_auto, fd_grenze_anheben, fd_lage, freigeben, lage, reservieren, reserviert, start_entscheiden, verworfen, zuruecksetzen
geocache.py            get, groesse, leeren, put
geoip.py               ist_privat, lookup
geschuetzt.py          lage, ruhend, vermerken, verschlossen, zuruecksetzen
highlights.py          check, new_state, observe, score, zustand
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kennzahlen.py          einwertig, prometheus, prozess, stand, veroeffentlichen, zeile
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
kickapi.py             app_token, broadcaster_id, channel_info, class PusherGeschlossen, configure, naechster_cluster, oauth_exchange, pusher_fehler, pusher_lage, pusher_pause, pusher_url, schliessgrund, search_category, send_message, slug, timeout_user, update_channel, user_token
kindprozess.py         alle_beenden, ausfuehren, beenden, lage, zuruecksetzen
kiwahl.py              backend, lokal_stand, lokal_zuerst, normal, provider
lagebild.py            bauen, restream_lage
lastvorsorge.py        freie_kerne, jung, startstufe
laufstand.py           befehl, veraltet, vergleich
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
livecache.py           aufraeumen, aufraeumen_faellig, dauer, einflug, frisch, holen, setzen, statistik, zaehle, zaehler_zuruecksetzen
livefolge.py           beste_url, braucht_url_nachschlag, hat_stream_url, last_dehnung, live_gesehen, offline_bestaetigt, poll_abstand, ruhezeit
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             fuer_log, redact_cookie_zeilen, redact_pull_urls, redact_stream_urls, url_ohne_zugang
logschleuse.py         class Schleuse, einreihen, entkoppeln, nachziehen, schwaerzen, stoppen, synchrone_handler, verloren, wartend, zuruecksetzen
looplag.py             bremser, erfassen, lage, spaeher_starten, stelle_aus_rahmen, takt, zuruecksetzen
loyalty.py             award_chat, award_return, configure, enabled, leaderboard, rank_for, status
mariadbumzug.py        class UmzugAbgebrochen, env_setzen, geoeffnet_von, in_benutzung, quelle_zaehlen, umziehen, vergleichen, ziel_zaehlen
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
meldetakt.py           erfolg, gestoert, melden, zuruecksetzen, zusatz
memeklip.py            class Fenster, frage, lies_urteil, soll_clippen
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
modki.py               frage, lies_klassifikation, lies_schimpfwoerter
modstats.py            ist_moderation, plattform, quellen, verdichte, zaehlt
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
oauthredirect.py       configure, public_base_url, redirect_env, redirect_public, redirect_source, redirect_uri
outcomes.py            get_outcome_breakdown
overlaytext.py         configure, latest_popularity, ov_atomic_write, ov_bar, ov_oneline, overlay_src_ok
persona.py             —
piper_voices.py        available, bin_pfad, configure, data_dir, list_voices, resolve, resolve_model_path, roots, voice_dirs, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
profildetail.py        datum, felder, kennzahlen, kontotyp, verlauf
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
prueflage.py           fuer_healthz, lage, merken, uebersicht, vergessen
qrsvg.py               qr_svg
quellprobe.py          empfehlung, form, kurz, main, maske, messen, probe_durchreicher, probe_ffprobe, probe_html, probe_ytdlp, ttl
quellstat.py           lage, zaehlen, zuruecksetzen
reccmd.py              build_recording_cmd, configure
recdb.py               configure, find_recordings_by_fingerprint, get_all_checks, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
resolvergrund.py       http_grund, quelle_lage, quelle_laut, text
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       betroffene_ziele, ein_start_je_ziel, fenstergroesse, freigeben, http_url, looks_like_source_expired, normalize_ingest, slot_belegt, startend, url_host
restreamcfg.py         active_platforms, aktiv, bereite_ziele, bruecke, bruecke_luecke, bruecke_offline, chat_src_ok, discord_invite, enabled, ingest, key_gesetzt, kick_channel_url, overlay, stall_timeout, verify, verify_karenz, verify_misses, verify_takt, yt_oauth_configured, ziel
restreamcmd.py         build, configure, drossel_avatar_aus, drossel_bitrate, drossel_canvas, drossel_fps, drossel_preset, drossel_zusatz, fueller, quell_eingang, schriftart, zubringer
restreamgesundheit.py  blind_markieren, frische_tee_fehler, marke_setzen
restreamstate.py       guard, haken, laufende, layout_mode, mgr
restrend.py            rising_trend
retention.py           scan
revenue.py             is_revenue_platform, normalisieren, sql_in
schema.py              anlegen, create_schema, index_sicher, kollation_angleichen, modultabellen, parameter, spalten_nachziehen
schemastand.py         lege_an, lies, pruefe, schreibe, streng
schnappschuss.py       class Schnappschuss
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendebruecke.py        class Bruecke, class TsUmschreiber, ist_keyframe, pat_pmt_pid, pes_zeit, pid, pmt_stroeme, pmt_urteil, video_pid, weiche_grund
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sicherpfad.py          pruefe_unter, sicher_join, sicherer_name, unter
sicherungspruefung.py  archiv_lesbar, dump_vollstaendig, pruefen
speicherpflege.py      abgelaufene_weg, alte_stempel_weg, groessen
sqldialekt.py          bei_konflikt
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
storage.py             cleanup, forecast, stats
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
suche.py               universal_search
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
systemprobe.py         active_recorder, ai_alive, ai_calls_total, cache_leeren, cached_probe, configure, cpu_load_snapshot, disk_pct, recorder_pref, recordings_dir, redis_alive, redis_url, redis_version
telegramfehler.py      dauer_text, grund, ist_fehler, ist_telegram_chat, text, zuruecksetzen
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tgmarkdown.py          html_zu_md, teilen
tiktokcheck.py         account_exists, configure
tiktokheaders.py       configure
tonspur.py             class Fehlschlag, garantie, garantie_cmd, hat_ton, hat_tonspur, ist_tonlos_fehler, nachruest_cmd, pruef_cmd, pruefen, sichern, stille_eingabe
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
tunnelwacht.py         lage, meldung, probe, probe_cmd
twitchoauth.py         access_token, authorize_url, configure, create_clip, exchange_code, forget, login_name, search_category, status, timeout_user, update_channel
updater.py             ausfuehrbar_im_archiv, build_plan, check, class Plan, class UpdaterConfig, commit_zip_url, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, rechte_angleichen, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                datei_in
version.py             build_stamp, changelog, current, latest, summary_line
videoteil.py           configure, dauer, ist_kaputter_container, kopier_teilen, neu_kodieren, platz_reicht, reparieren, wegwerfen, zeitstempel_richten, zu_gross
webserver.py           bindung, ist_loopback, schema, threads, tls_lage, waehle
whispercfg.py          geladen, name, verfuegbar, waehle
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytdlpurl.py            nur_frische, urls_aus_json
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status, upload_clip
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DatabaseAgent, class DiskAgent, class GrafanaAgent, class HealthAgent, class LearningAgent, class PrometheusAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
knowledge.py           class KnowledgeGraph
llm.py                 class BudgetExhausted, class LLMRuntime
memory.py              class Memory
report.py              weekly
router.py              class Task, class TaskRouter, class Unhandled
rules.py               class Rule, class RulesEngine
scheduler.py           class Scheduler
semantic.py            class SemanticMemory
state.py               class Entity, class StateMachine
test_bughunt.py        db_conn, main
test_m1.py             main
test_m3.py             main
test_m4.py             main
test_m5.py             main
test_m6.py             class LlamaCppMock, main
test_m7.py             db_conn, main
```

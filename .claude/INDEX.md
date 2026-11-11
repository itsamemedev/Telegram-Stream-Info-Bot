# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
 10979  GET              /                                                dashboard
 13036  GET              /api/abo/status                                  api_abo_status
 12990  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 11767  GET              /api/automation/status                           api_automation_status
 11789  POST             /api/automation/toggle                           api_automation_toggle
 21574  GET              /api/channel/categories                          api_channel_categories
 21580  POST             /api/channel/set                                 api_channel_set
 21427  GET              /api/channels/status                             api_channels_status
 21101  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 21084  GET              /api/clips                                       api_clips
 21130  POST/DELETE      /api/clips/clear                                 api_clips_clear
 21002  GET              /api/debug/threads                               api_debug_threads
 13001  GET              /api/events                                      api_events
 12480  GET              /api/events/stream                               api_events_stream
 12307  GET              /api/health                                      api_health
 21043  POST             /api/highlights/config                           api_highlights_config
 10909  POST             /api/login                                       dashboard_login_submit
 13326  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 12395  GET              /api/notify/status                               api_notify_status
 12406  POST             /api/notify/test                                 api_notify_test
 13090  GET              /api/proxy/heatmap                               api_proxy_heatmap
 13067  GET              /api/proxy/trend                                 api_proxy_trend
 21150  GET              /api/tts/<fn>                                    api_tts_file
 21924  GET              /api/upload_window                               api_upload_window
 12597  GET              /archive/<int:eid>/download                      archive_download
 12625  GET              /download/<int:recording_id>                     download
 12554  GET              /health                                          health
 20909  GET              /healthz                                         healthz
 10900  GET              /login                                           dashboard_login_page
 10934  GET              /logout                                          dashboard_logout
 10941  GET              /manifest.webmanifest                            pwa_manifest
 21897  GET              /overlay                                         overlay_page
 10965  GET              /pwa-icon-<variant>.png                          pwa_icon
 10951  GET              /sw.js                                           pwa_service_worker
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
   125  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   139  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    60  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   154  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
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
   222  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   242  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   269  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
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
   229  POST             /api/overlay/config                              api_overlay_config   [nc/routes/overlay.py]
   212  POST             /api/overlay/event                               api_overlay_event   [nc/routes/overlay.py]
   121  GET              /api/overlay/state                               api_overlay_state   [nc/routes/overlay.py]
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
   522  POST             /api/restream/<int:rid>/start                    api_restream_start   [nc/routes/restream.py]
   539  POST             /api/restream/<int:rid>/stop                     api_restream_stop   [nc/routes/restream.py]
   591  GET              /api/restream/chatfeed                           api_restream_chatfeed   [nc/routes/restream.py]
   444  POST             /api/restream/create                             api_restream_create   [nc/routes/restream.py]
   265  GET              /api/restream/deck                               api_restream_deck   [nc/routes/restream.py]
   165  GET              /api/restream/health                             api_restream_health   [nc/routes/restream.py]
   613  POST             /api/restream/layout                             api_restream_layout   [nc/routes/restream.py]
   413  GET              /api/restream/list                               api_restream_list   [nc/routes/restream.py]
   134  POST             /api/restream/report                             api_restream_report   [nc/routes/restream.py]
   552  POST             /api/restream/start_all                          api_restream_start_all   [nc/routes/restream.py]
   578  POST             /api/restream/stop_all                           api_restream_stop_all   [nc/routes/restream.py]
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
   237  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   458  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   487  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   407  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   420  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   516  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   393  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   268  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   313  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   337  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   324  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   164  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   282  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   133  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   374  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   429  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
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

## Discord-Slash-Commands in discordbot.py (67)

```
  2272  /about                  Ueber diesen Bot
   976  /ai                     
  2272  /aireset                KI-Kontext zuruecksetzen
  1391  /ask                    
  1077  /assign_role            
  1127  /ban                    
  2227  /botstats               
  2272  /brain                  Brain-Lage: Regeln, Agenten, Empfehlungen
  2272  /bulkadd                Mehrere User auf einmal tracken · a b c
  2272  /cleanup                Alte Aufnahmen aufraeumen
  1657  /clearwarns             
  2191  /clip                   
  2176  /clipoftheweek          
  1527  /clips                  
  2272  /cookies                Cookie-Status — mit 'holen' selbst beziehen · [holen]
  1032  /create_category        
  1003  /create_channel         
  1067  /create_group           
  1042  /create_role            
  1018  /create_voice           
  1268  /daily                  
  2272  /diag                   Vollstaendige Diagnose
  2272  /einnahmen              Einnahmen und Spenden
  1420  /event                  
  1462  /events                 
  1567  /follow                 
  1556  /help                   
  1117  /kick                   
  1243  /leaderboard            
  2272  /live                   Live-Status sofort pruefen · @user
  1514  /livenow                
  2272  /logs                   Letzte Fehler aus dem Log
  2272  /pause                  Tracking pausieren · @user
  1542  /post_test              
  1352  /profile                
  1149  /purge                  
  2272  /quelle                 Stream-Quellen eines Live-Nutzers messen (alle Wege, ffprobe
  2272  /quota                  Speicher-Quota
  1230  /rank                   
  1502  /recstatus              
  1087  /remove_role            
  2272  /report                 Azrael-Sentinel-Wochenreport
   989  /restream_status        
  2272  /resume                 Tracking fortsetzen · @user
  1097  /set_channel_perms      
  1192  /setup_community        
  1209  /setup_targets          
  1488  /spenden                
  1599  /stats                  
   948  /status                 
  2272  /stoprec                Laufende Aufnahme sauber beenden · @user
  1695  /streaminfo             
  2272  /summary                Tageszusammenfassung
  2272  /sysres                 System-Ressourcen
  2272  /teststream             Recorder-Selbsttest · @user
  2272  /tiktok                 Profil-Analyse eines TikTok-Accounts · ‹name›
  1137  /timeout                
  1667  /topstreamers           
  2272  /topusers               Top-Streamer nach Aufnahmen
   878  /track                  
  2272  /track_exact            Exakten Usernamen tracken (ohne Korrektur) · ‹name›
   961  /tracklist              
  1581  /unfollow               
  2272  /unpause                Auto-pausierte Quelle wieder aktivieren · @user
   910  /untrack                
  1620  /warn                   
  1643  /warnings               
```

## Discord-Events in discordbot.py (4)

```
  2435  on_member_join
  2392  on_message
  2293  on_raw_reaction_add
  2470  on_ready
```

## Top-Level-Symbole in telegramversand.py (2 Funktionen)

```
    60-75     konfiguriere
    78-533    split_and_send_video
```

## Top-Level-Symbole in discordbot.py (54 Funktionen)

```
  1772-1823   _award_xp
   535-562    _bereich_umziehen
   482-492    _clip_kopieren
  1994-2023   _clip_week_leader
  2047-2061   _clipoftheweek_loop
  2587-2649   _community_events_loop
  1729-1751   _dc_client
  1754-1763   _dc_offen
  2689-2724   _disc_automod_check
   408-413    _disc_sprache_setzen
  1826-1874   _discord_ai_automod
   684-723    _discord_automod
  1877-1897   _discord_azrael_reply
  2064-2546   _discord_run_once
   243-301    _discord_start
   304-358    _ensure_discord_invite
  2552-2584   _ensure_error_channel
   429-442    _ensure_rank_roles
   841-855    _ensure_team_roles
  2652-2682   _error_channel_loop
   733-737    _guard
   653-681    _handle_voice_ai
   416-426    _is_admin
   507-532    _link_video
  1942-1953   _liveboard_loop
   740-773    _on_level_up
   649-650    _par_chat_id
  2026-2044   _post_clip_of_week
  1956-1974   _post_weekly_digest
   445-471    _provision_base_channels
  1494-1588   _reg_betrieb
  1163-1257   _reg_community_setup
  1260-1341   _reg_daily_profil
  1384-1481   _reg_frage_events
   935-991    _reg_info
  1109-1160   _reg_moderation
  1344-1381   _reg_profil
  1058-1106   _reg_rollen
   994-1055   _reg_server
  1484-1491   _reg_spenden
  1591-1678   _reg_streamer
  1681-1726   _reg_system
   869-932    _reg_tracking
   808-838    _run_tg_handler
   636-646    _tracked_usernames
   160-222    _uebernehmen
   495-504    _umzugsmarken
  1906-1939   _update_liveboard
  1977-1991   _weekly_digest_loop
   474-479    _ziel_guild
   565-607    _ziele_abgleichen
   616-633    _ziele_sync_loop
   610-613    _ziele_takt_min
   225-228    starte
```

## Top-Level-Symbole in bot.py (592 Funktionen, 4 Klassen)

```
 26990-27012  _abbruch_datenbank_unlesbar
  2826-2827   _abo_key
  2847-2865   _abo_probe_dump
 27108-27124  _abschied_wachen
 27127-27145  _abschluss
 17199-17206  _ad_allowlist
 18361-18367  _agent_for
 18370-18386  _ai_telemetry
 18883-18901  _alert
 22792-22842  _alert_monitor_loop
 19562-19619  _alte_beilagen_einsammeln
 23224-23286  _announce_loop
  3726-3736   _anthropic_key
  3743-3745   _anthropic_model
 10543-10546  _arg_int
  2818-2823   _as_dict
 26676-26685  _async_exc_handler
 19064-19086  _audio_tap_cmd
 20075-20134  _audio_tap_melden
 19100-19124  _audio_tap_sammler
  9889-9926   _aufnahme_beim_stopp_sichern
 19504-19525  _aufnahme_chat_ausklang
 19488-19501  _aufnahme_chat_beginnen
 19647-19668  _aufnahme_chat_dienst
 19841-19894  _aufnahme_chat_einarbeiten
 19483-19485  _aufnahme_chat_modus
 19671-19720  _aufnahme_chat_nachtrag
 19528-19559  _aufnahme_chat_vormerken
 19638-19644  _aufnahme_chat_wecken
 25923-25925  _aufnahme_deckel
 19723-19744  _aufnahme_fertigmachen
 23461-23514  _aufnahme_nach_discord
  9929-9947   _aufnahme_platz_frei
  9832-9859   _aufnahme_verteilen
 27072-27092  _aufnahmen_abschliessen
 27015-27069  _aufraeumen
 10742-10811  _auth_cookie
 10700-10738  _auth_guard
  2053-2058   _auto_on
 20761-20779  _auto_restream_loop
 14671-14713  _avatar_frames_laden
 17249-17262  _azrael_brain_kontext
 24420-24435  _azrael_broadcast_reply
 24320-24342  _azrael_chat_reply
 24292-24317  _azrael_chat_should_reply
 24348-24350  _azrael_gate_cfg
 18391-18405  _azrael_live_state
 21810-21824  _azrael_overlay_state
 18765-18819  _azrael_proactive_loop
 18209-18265  _azrael_reaction_to_chats
 24353-24360  _azrael_reply_all_chats
 24279-24289  _azrael_self_names
 24388-24417  _azrael_send_to
 14632-14668  _azrael_spricht
 14979-14992  _azrael_stimme_stumm
 18411-18432  _azrael_system
 22926-22929  _backup_active
 23007-23020  _backup_loop
 26012-26016  _betrieb
 26749-26758  _brain_crowdsec_snap
 26917-26920  _brain_db_health
 22713-22722  _brain_growth_loop
 11158-11185  _brain_growth_snapshot
  2737-2771   _brain_hint_delay
 26821-26856  _brain_moderation_snap
  6732-6760   _brain_notify
 26923-26945  _brain_recording_snap
 26761-26818  _brain_restream_health
 26948-26961  _brain_tiktok_status_snap
 12459-12476  _browser_push
  6772-6859   _build_daily_summary
 15026-15030  _build_restream_cmd
  5484-5511   _can_stop_tracking
  2166-2188   _capture_set_cookies
 13144-13147  _cfg_get
 13150-13152  _cfg_set
 21535-21570  _channel_set_all
 13723-13726  _chat_connected
 13729-13745  _chat_disconnected
 19632-19635  _chat_einarbeiten_async
  9337-9359   _chat_is_forum
 19452-19477  _chat_listener_abbauen
  9499-9534   _chat_migriert
  9537-9538   _chat_migriert_async
 13765-13767  _chat_sanitize
 13708-13720  _chat_stat
 13748-13751  _chat_stats_snapshot
  4049-4061   _check_ai_models_sync
 11440-11483  _classify_pool_anonymity
 11486-11503  _classify_pool_anonymity_bg
   906-928    _claude_chat_sync_metered
 10575-10581  _client_ip
 23919-23933  _clip_chat_ass
 23370-23404  _clip_prune
 23407-23417  _clip_recfile_for
 23839-23907  _clip_schneiden
 23936-23942  _clip_should_velocity
 23517-23602  _clip_to_discord
 19812-19817  _clips_abwarten
  3930-3939   _close_ai_session
 24466-24481  _cohost_broadcast
 24451-24452  _cohost_cfg
 24507-24519  _cohost_fire_highlight
 24455-24463  _cohost_gate
 24484-24504  _cohost_highlight
 11088-11090  _conv_messages
  7156-7217   _cookie_alarm_loop
  2256-2257   _cookie_autofetch_info
  2240-2244   _cookie_autorefresh_info
 26383-26405  _cookie_bezug_loop
 26408-26433  _cookie_bezug_runde
  2143-2147   _cookie_header
 10584-10589  _cookie_sicher
  2269-2283   _cookies_selbst_holen
  4270-4272   _create_index_safe
 22256-22370  _crowdsec_status
 22202-22253  _crowdsec_via_lapi
 22106-22124  _cscli_bin
 22133-22146  _cscli_path
  7040-7067   _daily_summary_loop
 22164-22181  _darf_journal_lesen
  3251-3276   _darf_ytdlp_nachschlagen
 12640-12661  _dashboard_adresse
  1505-1535   _dashboard_trackings_umziehen
 23910-23916  _datei_weg
 22766-22789  _db_maintenance_loop
  6990-7037   _db_vacuum_loop
 17222-17246  _detect_foreign_ad
  1733-1744   _diag_path_owner
 18670-18715  _director_finalize
 20064-20071  _director_for
 18619-18667  _director_mark
 23752-23755  _disc_state_get
 23758-23765  _disc_state_set
 22694-22703  _discord_bot_starten
 22657-22668  _discord_einladung_merken
 22706-22710  _discord_invite
 22671-22691  _discord_kontext
 23713-23749  _discord_live_thread
 18822-18834  _discord_notify
 22629-22654  _discord_ops_alert
 23613-23709  _discord_post_user
 23289-23295  _discord_stop
  7070-7151   _disk_alarm_loop
 26306-26357  _disk_autoclean
 26531-26544  _disk_guard_loop
 14610-14617  _drossel_hoeher
 14606-14607  _drossel_stufe
 14620-14628  _drossel_zuruecksetzen
 12817-12819  _dump_all_threads
 26019-26033  _einstellungen_startzeile
 11366-11429  _enrich_proxies_with_geo
  2312-2373   _ensure_cookie_file_netscape
  9428-9431   _ensure_notify_topic
 11610-11647  _ensure_proxy_ready
  9369-9390   _ensure_topic
   747-749    _env_int
   752-754    _env_int_range
 18867-18880  _event_webhook
 13491-13504  _evolution_loop
  6173-6207   _extract_file_payload
  2445-2447   _extract_urls_from_streamurl_node
 22149-22156  _f2b_sudo_hint
  1491-1502   _fanout_ziele
 27148-27211  _fatal_vom_botteil
 25928-25943  _fd_grenze_anheben
  4944-4954   _fehler_text
 11267-11285  _fetch_proxy_list
 19421-19449  _fetch_tiktok_room_id
   832-835    _ff_cmd
 19825-19838  _ffprobe_masse
 14554-14570  _fifo_schreiber_wecken
 14364-14369  _find_chromium
  3646-3648   _find_external_recorder
  2450-2452   _find_stream_urls
 13195-13220  _fire_webhooks
  8035-8044   _fork_safe
   939-952    _freeai_chat_sync_metered
 22195-22199  _geo_lookup_ips
  3918-3927   _get_ai_session
  7868-7908   _get_live_info
  3102-3109   _get_resolve_semaphore
  8534-8954   _handle_single_tracking
 26128-26130  _hb
 26133-26150  _hb_while
 10815-10832  _herkunft_guard
 13779-13781  _highlight_cfg
 13784-13813  _highlight_observe
 14415-14423  _htmlov_bild_schreiben
 14393-14412  _htmlov_dauerbrowser
 14372-14390  _htmlov_screenshot_cmd
 19126-19136  _httpx_proxy
 13228-13240  _in_quiet_hours
 26976-26987  _init_db_oder_abbruch
 27795-27826  _install_fast_eventloop
 10438-10492  _install_fast_json
 12822-12838  _install_faulthandler
 20812-20821  _intel_ensure_schema
 20864-20899  _intel_index_loop
 20833-20848  _intel_index_one
 20824-20830  _intel_semantic
  5469-5482   _is_authorized
  8387-8408   _is_dead
  2435-2437   _is_hevc
 22184-22186  _is_private_ip
  1952-1959   _is_process_running
  6762-6769   _is_quiet_hours
  1393-1402   _is_upload_window
  4809-4824   _iso
 10592-10598  _ist_lokal
 10527-10540  _json_error_handler
  6984-6985   _kick_broadcaster_id
  8262-8269   _kick_cluster_gefunden
  8197-8259   _kick_cluster_weiter
  6896-6938   _kick_follower_count
  6880-6883   _kick_slug
 12272-12279  _kick_user_token
  8167-8194   _kick_ws_pause
 26964-26973  _kickmod_boot
  4354-4357   _kind_from_filename
 13257-13259  _latest_popularity
  1889-1898   _laufstand
 26491-26528  _laufstand_loop
 26052-26090  _leistung_erheben
  7742-7769   _link_video_senden
 20470-20519  _live_react_loop
 20137-20459  _live_react_worker
  3494-3608   _live_status_aufloesen
 18268-18279  _live_transcript_push
 20461-20468  _live_users
 18718-18762  _living_title_loop
 22932-23004  _local_backup_scan
  4749-4772   _lock_update
 10509-10523  _log_5xx
 26093-26125  _log_schleuse_pruefen
   822-829    _log_sicher
 15038-15050  _looks_like_codec_err
 15033-15035  _looks_like_source_expired
  8085-8115   _loop_fehler
 12842-12851  _loop_heartbeat
 25834-25867  _loop_lag_monitor
 25881-25901  _loop_stockung_melden
 25904-25914  _loop_takt_starten
 12854-12927  _loop_watchdog_thread
 18145-18162  _loyalty_add
 18136-18142  _loyalty_get
 18165-18173  _loyalty_top
  5151-5170   _manual_status
  8410-8411   _mark_dead
 11886-11902  _marketing_loop
 24367-24385  _maybe_handle_command
 26630-26654  _maybe_hype_clip
 23339-23367  _meme_klassifizieren
 19747-19809  _meme_zusammenschnitt
  4257-4262   _migrate_columns
 24649-24660  _mod_is_exempt
 24663-24668  _mod_warn_first
 24671-24674  _mod_warn_text
 13548-13567  _modlog
 13531-13545  _modlog_schreiben
  1089-1091   _multistream_targets
  3279-3315   _nachschlag_ytdlp
  8047-8048   _nc_create_subprocess_exec
  8051-8052   _nc_create_subprocess_shell
 12209-12226  _news_loop
 13590-13592  _normalize_ingest
  2668-2685   _note_check_duration
  9422-9425   _notify_topic_name
  2872-2878   _offline_ergebnis
  3318-3341   _ohne_url_melden
 18294-18302  _oracle_memories
 18568-18602  _oracle_memorize
 18305-18318  _oracle_persona
 18287-18291  _oracle_recent_text
 13988-13989  _ov_atomic_write
 13979-13981  _ov_bar
 17125-17137  _ov_clip_text
 13984-13985  _ov_oneline
 21861-21890  _overlay_push
 14318-14361  _overlay_render_size
 13659-13663  _overlay_session_reset
 21826-21828  _overlay_src_ok
 13998-14010  _overlay_takt
 17209-17219  _own_invites
 14313-14315  _parse_size
 22378-22458  _parse_ssh_attacks
  7418-7451   _pause_resume_cmd
  2194-2238   _persist_refreshed_cookies
  2097-2129   _pick_checked_pull_proxy
 10629-10642  _pin_auth_value
 10689-10690  _pin_clear_fail
 10669-10672  _pin_locked
 10675-10686  _pin_note_fail
 10645-10666  _pin_ok
 21668-21693  _piper_pick_model
 21753-21804  _piper_say
 13157-13192  _post_json_threaded
 14292-14310  _probe_video_size
  1980-1997   _proc_is_recorder
 11579-11607  _proxy_pool_refresh_loop
  2063-2094   _proxy_report_recording
  9093-9166   _pruef_runde
  9052-9090   _pruefstand_melden
 25963-25974  _pruefung_verworfen
 12807-12809  _prune_stall_dumps
 11956-12128  _public_stats
  2260-2266   _pull_proxy_still
 18838-18864  _push_notify
 10879-10881  _pwa_dir
 11336-11351  _quick_validate_proxy
 13223-13225  _quiet_hours_config
 10844-10877  _rate_guard
 18106-18112  _react_warn
  7955-7994   _reap_proc
  9762-9829   _rec_auto_abschalten
  9709-9759   _rec_frueh_getrennt
  9578-9654   _rec_kategorie_melden
  9657-9706   _rec_totstreak_fortschreiben
  2708-2730   _record_check_outcome
   817-819    _redact_stream_urls
 11506-11576  _refresh_proxy_pool
  2485-2576   _resolve_via_html
  2881-3079   _resolve_via_webcast_api_v2
  3142-3227   _resolve_via_ytdlp
 23976-24105  _resolve_youtube_ingest
  2461-2482   _resolver_stumm
 13642-13653  _restream_active_sources
 14716-14843  _restream_avatar_feeder_start
 14846-14856  _restream_avatar_feeder_stop
 19897-20028  _restream_chat_guardian
 13816-13888  _restream_chat_push
 13965-13974  _restream_chat_push_async
 26859-26914  _restream_durchreicher
 14426-14551  _restream_html_overlay_start
 14573-14593  _restream_html_overlay_stop
 13601-13624  _restream_overlay_files
 20523-20555  _restream_platform_state
 20723-20758  _restream_resume_after_restart
 13919-13936  _restream_soll_schreiben
 13939-13962  _restream_status_schreiben
 14904-14976  _restream_tts_enqueue_wav
 14254-14286  _restream_tts_feeder
 14251-14252  _restream_tts_fifo_path
 14859-14886  _restream_tts_start
 14888-14902  _restream_tts_stop
 20561-20720  _restream_verify_loop
 22897-22909  _retention_loop
 22891-22894  _retention_scan
  2829-2831   _room_is_abo
  6211-6328   _run_ai_call
 12950-12963  _run_async_from_flask
 22189-22192  _run_priv
 27783-27791  _run_selfcheck_and_exit
 22912-22923  _s3_client
  8437-8507   _safe_send
  5077-5093   _sample_net_throughput
  2774-2804   _schedule_next_check
 22845-22888  _scheduler_loop
  4265-4267   _schema_pk
 12967-12972  _scraper_session
 24677-24716  _screen_full
 12323-12360  _sec_headers
  2440-2442   _select_stream_from_data_section
 27503-27780  _selfcheck
  9434-9468   _send_live_notice
  1416-1420   _should_defer_upload
 23420-23458  _shrink_for_discord
 10884-10896  _sicheres_ziel
 22725-22763  _sicherheits_erinnerung_loop
 26551-26568  _sign_health_check
 26571-26590  _sign_health_loop
  4827-4852   _sitzung_bestimmen
  8064-8075   _spawn
 28214-28244  _spawn_from_flask
 25977-25983  _speicher_maps
 25986-26001  _speicher_pflegen
 19138-19418  _start_chat_listener
 25946-25960  _start_gesperrt
 12930-12947  _start_loop_watchdog
 12155-12204  _stats_loop
 12134-12137  _stats_output_path
 12140-12152  _stats_write
 21705-21719  _stimme_saubern
 21726-21750  _stimme_schon_gesagt
  9033-9049   _storage_cleanup_loop
 26610-26617  _story_for
  3671-3677   _stream_url_expiry
  3679-3684   _stream_url_ttl
 17172-17179  _streamer_persona_get
 23029-23181  _system_backup
 23190-23220  _system_backup_loop
 12767-12785  _task_auf_bot_schleife
 25514-25530  _telegram_befehlsmenue
  8118-8164   _telegram_polling_fehler
  1461-1488   _telegram_ziele
 11288-11327  _test_proxy
 11834-11850  _testpush_resolve_live
 19820-19822  _text_schreiben
  9486-9496   _tg_migriert_laden
  9482-9483   _tg_migriert_pfad
  8413-8434   _tg_sprache_setzen
  9306-9316   _tg_topics_load_into_mem
  9303-9304   _tg_topics_path
  9318-9325   _tg_topics_save
 10601-10611  _token_ok
  9393-9409   _topic_anlegen
  9328-9335   _topic_forget
 13243-13254  _tracking_max_duration
  4562-4576   _tracking_remove_cleanup
  4593-4605   _tracking_resume_cleanup
  1791-1814   _try_attach_file_handler
 21695-21703  _tts_cleanup
 11810-11814  _tunnel_effective
 26360-26380  _tunnel_lage
 26436-26488  _tunnel_wacht_loop
 21194-21247  _twitch_channel_status
 24719-24867  _twitch_chat_loop
 23771-23784  _twitch_clip_versuchen
 24530-24636  _twitch_eventsub_loop
  1581-1616   _upload_queue_abarbeiten
  1439-1459   _upload_queue_add
  1552-1554   _upload_queue_count
  1422-1431   _upload_queue_load
  1619-1641   _upload_queue_nachher
  1412-1414   _upload_queue_path
  1538-1542   _upload_queue_remove
  1433-1437   _upload_queue_save
  1545-1550   _upload_queue_update
  9862-9886   _upload_rest_sichern
  1556-1578   _upload_window_loop
  7928-7935   _uptime_s
 13578-13587  _url_host
  3344-3442   _url_nachschlag
   899-903    _usage_record_claude
 26724-26746  _v37_pause_source
 26688-26698  _v37_restream_restart
 26701-26721  _v37_unpause_source
  8336-8380   _verbindung_verloren
  6941-6972   _viewer_sample_loop
 10693-10696  _wants_html
  7938-7952   _warn_empty_env
 26171-26292  _watchdog_loop
 24251-24259  _wchat_thank_ok
 18906-18936  _whisper_get_model
  8025-8032   _whisper_native_section
 18093-18099  _whisper_pool
 19030-19062  _whisper_segments
 18938-18954  _whisper_stumm
 18957-19027  _whisper_transcribe
 14051-14208  _write_restream_overlay
 14013-14048  _write_restream_overlay_async
 24891-24990  _youtube_api_chat_loop
 21250-21353  _youtube_api_status
 21356-21423  _youtube_channel_status
 24993-25157  _youtube_chat_loop
 23787-23812  _youtube_clip_versuchen
 24111-24124  _youtube_restream_autoconfig
 24127-24151  _youtube_restream_autoconfig_inner
 24218-24246  _youtube_send
 21491-21532  _youtube_set_channel
 24154-24188  _yt_access_token
 24191-24206  _yt_live_chat_id
 24214-24215  _yt_sendrate_cfg
 24870-24885  _yt_timeout
  3126-3127   _ytdlp_detect_available
  3129-3140   _ytdlp_note_result
 12812-12814  _zombie_child_count
 26036-26049  _zustand_kennzahlen
  7804-7828   about
  4473-4477   add_ai_log_entry
  4390-4393   add_archive_entry
  5115-5117   add_archive_rule
  4855-4926   add_recording
  4537-4554   add_tracking
  6331-6364   ai
  4075-4161   ai_chat
  4195-4205   ai_history_append
  4207-4212   ai_history_clear
  4184-4193   ai_history_load
  4169-4182   ai_rate_limit_check
  6393-6401   aireset
 18435-18454  azrael_chat
 25162-25284  brain_cmd
  3687-3692   build_recording_cmd
  4557-4560   bulk_add_trackings
  7220-7279   bulkadd
  9169-9285   check_all_trackings
  4609-4621   claim_live_transition
 17265-18025  class KickModerator
 15053-17012  class RestreamManager
  4775-4776   class _AufnahmeLockVerloren
  8272-8333   class _KickClusterSuche
 11693-11735  classify_proxy_anonymity
  6439-6638   cleanup
  5405-5411   cleanup_old_recordings
  4800-4807   clear_recording
 23815-23836  clip_moment
  5067-5070   compute_storage_forecast
  7342-7415   cookies_cmd
  4528-4534   count_trackings_for_chat
  4460-4471   decide_preferred_recorder
  4400-4403   delete_archive_entry
  5119-5121   delete_archive_rule
  5868-6015   diag
 25396-25457  einnahmen_cmd
  5061-5064   find_recordings_by_fingerprint
  4421-4437   finish_recording_attempt
  4581-4583   get_all_active_trackings
  4488-4490   get_all_checks
  4928-4931   get_all_recordings
  5010-5012   get_all_tags_with_counts
  5038-5041   get_annotations_for_recording
  4395-4398   get_archive_entry
  5031-5034   get_bookmarked_recordings
  2300-2305   get_cookie_health
  4998-5004   get_event_log
  4444-4458   get_last_recording_attempt
  3445-3487   get_live_status
  5344-5347   get_manual_recordings
  5046-5049   get_or_compute_inspect_sync
  5446-5449   get_outcome_breakdown
  5017-5020   get_priority_poll_interval
  4439-4442   get_recent_recording_attempts
  4933-4936   get_recording_by_id
  5024-5027   get_recording_note
  3858-3887   get_redis
  4517-4520   get_stats
  5399-5403   get_storage_stats
  5139-5141   get_tiktok_status_distribution
  4623-4632   get_tracking_state
  4578-4579   get_trackings_for_group
  5360-5363   get_trash_recordings
  9950-10417  handle_recording_finished
 25506-25511  hilfe_cmd
  4280-4345   init_db
  5111-5113   list_archive_rules
  5653-5691   live
  8510-8532   live_check_worker
  3942-3985   llm_chat
  4008-4039   llm_chat_sync
  3993-4005   llm_list_models
  4957-4990   log_event
  1914-1947   log_recording_failure
  7565-7614   logs_cmd
 27214-27493  main
  6367-6390   on_ai_media
  7691-7717   on_ai_reply
  7772-7801   on_azrael_mention
  7833-7863   on_callback
  9541-9559   on_chat_migration
  7726-7739   on_link_video
 18460-18565  oracle_handle
  7454-7457   pause_tracking
  5459-5464   profile_keyboard
  5606-5650   quelle
  7516-7562   quota
  8956-9030   reaper_loop
  5135-5137   record_tiktok_status
  6406-6436   recstatus
  3889-3897   redis_get_json
  3900-3906   redis_set_json
 25533-25543  report_cmd
 11738-11740  report_proxy_result
  2579-2621   resolve_tiktok_live_stream
  5355-5358   restore_recording
  7460-7463   resume_tracking
  5124-5129   run_archive_rules
 25546-25814  run_bot
 12664-12758  run_flask
  5099-5102   sample_bandwidth_for_active
  4480-4486   save_tiktok_check
  4779-4798   set_recording_file
  4586-4590   set_tracking_paused
  5350-5353   soft_delete_recording
 25491-25503  spenden_cmd
  9565-9576   split_and_send_video
  5516-5558   start
  4405-4419   start_recording_attempt
  6641-6679   stats
  5289-5342   stop_manual_recording
  7466-7513   stoprec
  6865-6873   summary_cmd
  7617-7688   sysres
  6017-6161   teststream
  5560-5601   tiktok
  7282-7339   topusers
  5728-5785   track
  5693-5725   track_exact
  5799-5866   tracklist
  5173-5287   trigger_manual_recording
  4711-4746   try_acquire_recording_lock
  5366-5368   universal_search
 25460-25488  unpause_cmd
  5787-5797   untrack
 25287-25393  update_cmd
  5056-5059   update_recording_fingerprint
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
azraelkontext.py       ausfall, block, fakten, letzte_erinnerung, nachricht, restream_quellen, sicher, streamer_waehlen
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
crypto.py              addresses, erwartete_namen, fehlende_namen, gesetzte, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dashauth.py            erlaubt_offen, geschuetzt, host, lage, nur_lokal, offen_im_netz, zurueckgefallen
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbgesundheit.py        messen
dbrestore.py           archive, dump_aus_archiv, einsetzen, einspielen, vorbereiten
dbwartung.py           faellig_in, letzter_lauf, merken, stand_datei
dbwrap.py              class DatenbankUnlesbar, configure_db, datei_diagnose, db_async, db_conn, get_pool, set_pool
ddlsafe.py             ddl, ist_schon_da
defensecfg.py          bouncer_gesetzt, bouncer_key, geo_fehler, geo_fehler_setzen, lapi_host, lapi_port, lapi_url, server_lat, server_lon
director.py            class LiveDirector, configure
discordaufnahme.py     an, beschriftung, hochladen, teilen
discordlimits.py       aktuell_label, aktuell_mb, configure, describe, effective_upload_mb, gate_mb, guild_filesize_bytes, guild_limit_mb
discordrang.py         rang_fuer_level, slug, xp_fuer_level, xp_zu_level
discordstate.py        invite, state_get
discordziele.py        clip_kanal, clip_kanal_des_bereichs, clip_kanal_holen, eigene_kanaele, loeschbar, umzugsmarke, umzugsmarke_lesen
donations.py           configure, fmt_eur, kurse_aus_env, parse_number, source_allowed, summe_eur, to_eur, unknown_count, zeile_eur
donationsdb.py         manual_rows, manual_total, parse_eur
durchreicher.py        adresse, ist, main, nutzer_aus, werkzeug, werkzeuge, zieher_cmd, zieher_umgebung, zubringer_cmd
einstellungen.py       bekannt, class Abgelehnt, db_werte, geheim, gueltiger_name, in_umgebung_laden, katalog, pruefen, schutzgrund, setzen, startbericht, uebernehmen, uebersicht, zuruecksetzen
encodeschlange.py      lage, last_frei, parallel, platz, platz_sync
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
herkunft.py            entscheiden
highlights.py          check, new_state, observe, score, zustand
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kennzahlen.py          einwertig, prometheus, prozess, stand, veroeffentlichen, zeile
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
kickapi.py             app_token, broadcaster_id, channel_info, class PusherGeschlossen, configure, naechster_cluster, naechster_key, oauth_exchange, pusher_fehler, pusher_lage, pusher_pause, pusher_url, schliessgrund, search_category, send_message, slug, timeout_user, update_channel, user_token
kickzentrifugo.py      als_frame, antwort_fehler, class KickZentrifugoFehler, connect_cmd, fehler_code, ist_ping, kanal, lage, neue_client_id, neues_token, pause, refresh_cmd, subscribe_cmd, token_aus, ttl_aus, verbindung_body, ws_url_aus, zerlegen, zugang
kindprozess.py         alle_beenden, ausfuehren, beenden, lage, zuruecksetzen
kiwahl.py              backend, lokal_stand, lokal_zuerst, normal, provider
lagebild.py            bauen, restream_lage
lastvorsorge.py        freie_kerne, jung, startstufe
laufstand.py           befehl, veraltet, vergleich
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
linkvideo.py           abklingzeit_s, an, aufraeumen, ausgabe_lesen, befehl, bildunterschrift, configure, darf, grund, holen, ist_tiktok, links, max_dauer_s, sperre, werkzeug
livecache.py           aufraeumen, aufraeumen_faellig, dauer, einflug, frisch, holen, setzen, statistik, zaehle, zaehler_zuruecksetzen
livefolge.py           beste_url, braucht_url_nachschlag, hat_stream_url, last_dehnung, live_gesehen, offline_bestaetigt, poll_abstand, ruhezeit
livemeldung.py         live_an, live_aus
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
overlaybrowser.py      browser_cmd, class Dauerbrowser, class OverlayBrowserFehler
overlaytext.py         configure, latest_popularity, ov_atomic_write, ov_bar, ov_oneline, overlay_src_ok
persona.py             —
piper_voices.py        available, bin_pfad, configure, data_dir, list_voices, resolve, resolve_model_path, roots, voice_dirs, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
profildetail.py        datum, felder, kennzahlen, kontotyp, verlauf
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
prueflage.py           fuer_healthz, lage, merken, runde_gelaufen, uebersicht, vergessen
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
spendeninfo.py         krypto, paypal, paypal_url, stand, text
spendenziel.py         eingang, fenster_start, ist_monatlich, stand, summe, zeitraum, ziel_eur
sqldialekt.py          bei_konflikt
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
storage.py             class BestandUnbekannt, cleanup, forecast, notfall_raeumen, stats
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
suche.py               universal_search
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
systemprobe.py         active_recorder, ai_alive, ai_calls_total, cache_leeren, cached_probe, configure, cpu_load_snapshot, disk_pct, recorder_pref, recordings_dir, redis_alive, redis_url, redis_version
telegramfehler.py      dashboard_umzug, dauer_text, ersatz, grund, ist_fehler, ist_telegram_chat, migration_plan, migriert_erlaubt, nur_telegram, standardgruppe, text, zuruecksetzen
textmore.py            configure_banned_cap, pre_nachrichten, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tgmarkdown.py          html_zu_md, teilen
tiktokcheck.py         account_exists, configure
tiktokheaders.py       configure
tonspur.py             class Fehlschlag, garantie, garantie_cmd, hat_ton, hat_tonspur, ist_tonlos_fehler, nachruest_cmd, pruef_cmd, pruefen, sichern, stille_eingabe
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
tunnelwacht.py         lage, meldung, probe, probe_cmd
twitchoauth.py         access_token, authorize_url, configure, create_clip, exchange_code, forget, login_name, search_category, status, timeout_user, update_channel
updater.py             ausfuehrbar_im_archiv, build_plan, check, class Plan, class UpdaterConfig, commit_zip_url, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, rechte_angleichen, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
uploadschlange.py      angekommen, faellig, gleicher, nach_versuch, pause_s
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                datei_in
version.py             build_stamp, changelog, current, latest, summary_line
videoteil.py           configure, dauer, ist_kaputter_container, kopier_teilen, neu_kodieren, platz_reicht, reparieren, wegwerfen, zeitstempel_richten, zu_gross
webserver.py           bindung, ist_loopback, schema, threads, tls_lage, waehle
whispercfg.py          geladen, name, verfuegbar, waehle
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytdlpurl.py            nur_frische, urls_aus_json
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status, upload_clip
zeitglaetter.py        ausdruck, bsf_args, filter_text, verfuegbar
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
scheduler.py           class Scheduler, frische_intervalle
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
